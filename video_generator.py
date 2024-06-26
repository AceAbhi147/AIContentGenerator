import os
from moviepy.editor import VideoFileClip, AudioFileClip, ImageSequenceClip, TextClip, CompositeVideoClip, ColorClip
from moviepy.config import change_settings


change_settings({"IMAGEMAGICK_BINARY": r"C:\Program Files\ImageMagick-7.1.1-Q16-HDRI\magick.exe"})


class VideoGenerator:

    def __init__(self, image_folder, video_path, audio_path, audio_runtime, image_screen_time, prompts_and_images):
        self.image_folder = image_folder
        self.temp_video_name = os.path.join(video_path, "temp_video.mp4")
        self.final_video_name = os.path.join(video_path, "video.mp4")
        self.audio_file = os.path.join(audio_path, "audio.mp3")
        self.audio_runtime = audio_runtime
        self.image_screen_time = image_screen_time
        self.images_order = [image[1] for image in prompts_and_images]

    def __validate_images_and_sort(self):
        image_file = []
        for image in self.images_order:
            if image in os.listdir(self.image_folder):
                image_file.append(os.path.join(self.image_folder, image))
        return image_file

    def __create_caption(self, textJSON, framesize, font="Loma-Bold", color='yellow4', highlight_color='yellow',
                         stroke_color='black', stroke_width=1.5):
        full_duration = textJSON['end'] - textJSON['start']

        word_clips = []
        xy_textclips_positions = []

        x_pos = 0
        y_pos = 0
        line_width = 0  # Total width of words in the current line
        frame_width = framesize[0]
        frame_height = framesize[1]

        x_buffer = frame_width * 1 / 10

        max_line_width = frame_width - 2 * (x_buffer)

        fontsize = int(frame_height * 0.04)  # 4 percent of video height
        for index, wordJSON in enumerate(textJSON['text_contents']):
            duration = wordJSON['end'] - wordJSON['start']
            word_clip = (TextClip(wordJSON['word'], font=font, fontsize=fontsize, color=color,
                                  stroke_color=stroke_color, stroke_width=stroke_width)
                         .set_start(textJSON['start']).set_duration(full_duration))
            word_clip_space = TextClip(" ", font=font, fontsize=fontsize, color=color).set_start(
                textJSON['start']).set_duration(full_duration)
            word_width, word_height = word_clip.size
            space_width, space_height = word_clip_space.size

            if line_width + word_width + space_width <= max_line_width:
                # Store info of each word_clip created
                xy_textclips_positions.append({
                    "x_pos": x_pos,
                    "y_pos": y_pos,
                    "width": word_width,
                    "height": word_height,
                    "word": wordJSON['word'],
                    "start": wordJSON['start'],
                    "end": wordJSON['end'],
                    "duration": duration
                })

                word_clip = word_clip.set_position((x_pos, y_pos))
                word_clip_space = word_clip_space.set_position((x_pos + word_width, y_pos))

                x_pos = x_pos + word_width + space_width
                line_width = line_width + word_width + space_width
            else:
                # Move to the next line
                x_pos = 0
                y_pos = y_pos + word_height + 10
                line_width = word_width + space_width

                # Store info of each word_clip created
                xy_textclips_positions.append({
                    "x_pos": x_pos,
                    "y_pos": y_pos,
                    "width": word_width,
                    "height": word_height,
                    "word": wordJSON['word'],
                    "start": wordJSON['start'],
                    "end": wordJSON['end'],
                    "duration": duration
                })

                word_clip = word_clip.set_position((x_pos, y_pos))
                word_clip_space = word_clip_space.set_position((x_pos + word_width, y_pos))
                x_pos = word_width + space_width

            word_clips.append(word_clip)
            word_clips.append(word_clip_space)

        for highlight_word in xy_textclips_positions:
            word_clip_highlight = TextClip(highlight_word['word'], font=font, fontsize=fontsize, color=highlight_color,
                                           stroke_color=stroke_color, stroke_width=stroke_width).set_start(
                highlight_word['start']).set_duration(highlight_word['duration'])
            word_clip_highlight = word_clip_highlight.set_position((highlight_word['x_pos'], highlight_word['y_pos']))
            word_clips.append(word_clip_highlight)

        return word_clips, xy_textclips_positions

    def images_to_video(self):
        print("Generating video from images..................")
        images = self.__validate_images_and_sort()
        final_images = []
        idx = 0
        for curr_screen_time in self.image_screen_time:
            curr_image_idx = idx % len(images)
            for _ in range(curr_screen_time):
                final_images.append(images[curr_image_idx])
            idx += 1

        clip = ImageSequenceClip(final_images, fps=1)
        clip.write_videofile(self.temp_video_name, codec="libx264")
        print("Video generated and saved at " + str(self.temp_video_name) + "\n\n")

    def add_subtitles_and_audio_to_video(self, line_level_subtitles):
        print("Adding subtitles to the generated video.....................")
        input_video = VideoFileClip(self.temp_video_name)
        frame_size = input_video.size

        all_line_level_splits = []
        for line in line_level_subtitles:
            out_clips, positions = self.__create_caption(line, frame_size)

            max_width = 0
            max_height = 0

            for position in positions:
                x_pos, y_pos = position['x_pos'], position['y_pos']
                width, height = position['width'], position['height']

                max_width = max(max_width, x_pos + width)
                max_height = max(max_height, y_pos + height)

            color_clip = ColorClip(size=(int(max_width * 1.1), int(max_height * 1.1)),
                                   color=(64, 64, 64))
            color_clip = color_clip.set_opacity(0)
            color_clip = color_clip.set_start(line['start']).set_duration(line['end'] - line['start'])

            clip_to_overlay = CompositeVideoClip([color_clip] + out_clips)
            clip_to_overlay = clip_to_overlay.set_position(("center", frame_size[1] - max_height - 200))

            all_line_level_splits.append(clip_to_overlay)

        final_video = CompositeVideoClip([input_video] + all_line_level_splits)
        print("Subtitles added!!")

        # Set the audio of the final video
        final_video = final_video.set_audio(AudioFileClip(self.audio_file))
        print("Audio added!!")

        # Save the final clip as a video file with the audio included
        final_video.write_videofile(self.final_video_name, fps=24, codec="libx264", audio_codec="aac")

        os.remove(self.temp_video_name)
        print("Final Video generated and saved at " + str(self.final_video_name))
