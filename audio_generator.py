import gtts


class AudioGenerator:
    def generate_audio(self, audio_data, file_path):
        print("Generating audio")
        audio = audio_data['Story']
        if 'Lesson' in audio_data:
            audio += ' The Lesson - ' + audio_data['Lesson']
        audio_gtts = gtts.gTTS(audio)
        file_name = f'{file_path}/audio.mp3'
        audio_gtts.save(file_name)
        print("Audio Generated and Saved in: " + str(file_path))
