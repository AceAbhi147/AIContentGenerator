import cv2
import os
import math
from pydub import AudioSegment
from moviepy.editor import VideoFileClip, AudioFileClip, ImageSequenceClip, ColorClip
from PIL import Image


class VideoGenerator:

    def __init__(self, image_folder, video_path, audio_path):
        self.image_folder = image_folder
        self.video_name = f'{video_path}/video.mp4'
        audio_file = f'{audio_path}/audio.mp3'
        self.audio_file = audio_file
        audio_duration = len(AudioSegment.from_file(audio_file))
        self.audio_runtime = int(math.ceil(audio_duration / 1000))

    def __extract_numeric_suffix(self, filename):
        parts = filename.split('.')
        if len(parts) > 1:
            numerical_part = parts[0]
            try:
                return int(numerical_part)
            except ValueError:
                return 0
        return 0

    def old_images_to_video(self):
        images = sorted(os.listdir(self.image_folder), key=self.__extract_numeric_suffix)
        per_image_screentime = int(self.audio_runtime / len(images))
        avg_height = 0
        avg_width = 0
        for image in images:
            frame = cv2.imread(os.path.join(self.image_folder, image))
            height, width, layers = frame.shape
            avg_height += height
            avg_width += width

        avg_height = int(avg_height / len(images))
        avg_width = int(avg_width / len(images))

        video = cv2.VideoWriter(self.video_name, cv2.VideoWriter_fourcc(*'mp4v'), 1, (avg_width, avg_height))
        print("Screen time of each image: " + str(per_image_screentime))
        for image in images:
            img = cv2.imread(os.path.join(self.image_folder, image))
            img = cv2.resize(img, (avg_width, avg_height))
            for _ in range(per_image_screentime):
                video.write(img)

        cv2.destroyAllWindows()
        video.release()

    def images_to_video(self):
        images = [os.path.join(self.image_folder, img) for img in
                  sorted(os.listdir(self.image_folder), key=self.__extract_numeric_suffix)
                  if img.endswith(('.png', '.jpg', '.jpeg', '.webp'))]
        padded_images = []
        per_image_screentime = int(self.audio_runtime / len(images))
        for image in images:
            img = Image.open(image)
            padded_image = self.pad_image(img, (1920, 1080))

            if not os.path.exists(os.path.join(self.image_folder, 'padded')):
                os.makedirs(os.path.join(self.image_folder, 'padded'))
            padded_image_path = os.path.join(self.image_folder, 'padded', os.path.basename(image))
            padded_image.save(padded_image_path)
            for _ in range(per_image_screentime):
                padded_images.append(padded_image_path)

        clip = ImageSequenceClip(padded_images, fps=1)
        clip.write_videofile(self.video_name, codec="libx264")

    def pad_image(self, image, target_size):
        target_width, target_height = target_size
        background = Image.new('RGB', target_size, (0, 0, 0))
        width, height = image.size
        position = ((target_width - width) // 2, (target_height - height) // 2)
        background.paste(image, position)
        return background

    def combine_audio_and_video(self):
        video = VideoFileClip(self.video_name)
        audio = AudioFileClip(self.audio_file)

        video = video.set_audio(audio)
        video.write_videofile("testing.mp4")
