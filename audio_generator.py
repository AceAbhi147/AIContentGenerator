import os.path
import math
import gtts
from faster_whisper import WhisperModel
from pydub import AudioSegment


class AudioGenerator:
    def __init__(self, audio_data, audio_file_path):
        self.audio_data = self.get_audio_data(audio_data)
        self.audio_file_name = f'{audio_file_path}/audio.mp3'
        # self.model = WhisperModel("medium")
        self.audio_runtime = None
        self.subtitles_context = None

    def get_audio_data(self, audio_data):
        audio = ""
        if isinstance(audio_data, str):
            audio = audio_data
        elif isinstance(audio, dict):
            if 'Story' in audio_data:
                audio = audio_data['Story']
            if 'Lesson' in audio_data:
                audio += ' The Lesson - ' + audio_data['Lesson']
        return audio

    def get_existing_audio_file_runtime(self):
        if os.path.exists(self.audio_file_name):
            self.audio_runtime = self.get_audio_file_runtime()

    def get_audio_file_runtime(self):
        audio_duration = len(AudioSegment.from_file(self.audio_file_name))
        return int(math.ceil(audio_duration / 1000))

    def generate_audio(self):
        print("Generating audio")
        audio_gtts = gtts.gTTS(self.audio_data)
        audio_gtts.save(self.audio_file_name)
        self.audio_runtime = self.get_audio_file_runtime()
        print("Audio Generated and Saved in: " + str(self.audio_file_name))

    def get_word_timestamp(self):
        # segments, info = self.model.transcribe(self.audio_file_name, word_timestamps=True)
        # segments = list(segments)
        # word_timestamp = []
        # for segment in segments:
        #     for word in segment.words:
        #         word_timestamp.append({'word': word.word, 'start': word.start, 'end': word.end})
        self.subtitles_context = self.split_text_into_lines(self.get_sample_word_timestamp())

    def split_text_into_lines(self, word_timestamp):
        max_char = 30
        # max duration in seconds
        max_duration = 2.5
        # Split if nothing is spoken (gap) for these many seconds
        max_gap = 1.5

        subtitles = []
        line = []
        line_duration = 0
        line_chars = 0

        for idx, word_data in enumerate(word_timestamp):
            word = word_data["word"]
            start = word_data["start"]
            end = word_data["end"]

            line.append(word_data)
            line_duration += end - start

            temp = " ".join(item["word"] for item in line)

            # Check if adding a new word exceeds the maximum character count or duration
            new_line_chars = len(temp)

            duration_exceeded = line_duration > max_duration
            chars_exceeded = new_line_chars > max_char
            if idx > 0:
                gap = word_data['start'] - word_timestamp[idx - 1]['end']
                # print (word,start,end,gap)
                max_gap_exceeded = gap > max_gap
            else:
                max_gap_exceeded = False

            if duration_exceeded or chars_exceeded or max_gap_exceeded:
                if line:
                    subtitle_line = {
                        "word": " ".join(item["word"] for item in line),
                        "start": line[0]["start"],
                        "end": line[-1]["end"],
                        "text_contents": line
                    }
                    subtitles.append(subtitle_line)
                    line = []
                    line_duration = 0
                    line_chars = 0

        if line:
            subtitle_line = {
                "word": " ".join(item["word"] for item in line),
                "start": line[0]["start"],
                "end": line[-1]["end"],
                "text_contents": line
            }
            subtitles.append(subtitle_line)

        return subtitles

    def get_sample_word_timestamp(self):
        return [
            {
                "word": " Galileo",
                "start": 0.0,
                "end": 0.8
            },
            {
                "word": " was",
                "start": 0.8,
                "end": 1.06
            },
            {
                "word": " in",
                "start": 1.06,
                "end": 1.24
            },
            {
                "word": " a",
                "start": 1.24,
                "end": 1.4
            },
            {
                "word": " precarious",
                "start": 1.4,
                "end": 2.04
            },
            {
                "word": " situation",
                "start": 2.04,
                "end": 2.82
            },
            {
                "word": " in",
                "start": 2.82,
                "end": 3.1
            },
            {
                "word": " early",
                "start": 3.1,
                "end": 3.46
            },
            {
                "word": " 1600.",
                "start": 3.46,
                "end": 4.42
            },
            {
                "word": " He",
                "start": 4.9,
                "end": 5.12
            },
            {
                "word": " was",
                "start": 5.12,
                "end": 5.44
            },
            {
                "word": " worried",
                "start": 5.44,
                "end": 5.78
            },
            {
                "word": " about",
                "start": 5.78,
                "end": 6.16
            },
            {
                "word": " getting",
                "start": 6.16,
                "end": 6.56
            },
            {
                "word": " enough",
                "start": 6.56,
                "end": 6.92
            },
            {
                "word": " support",
                "start": 6.92,
                "end": 7.36
            },
            {
                "word": " from",
                "start": 7.36,
                "end": 7.66
            },
            {
                "word": " his",
                "start": 7.66,
                "end": 8.0
            },
            {
                "word": " patrons",
                "start": 8.0,
                "end": 8.42
            },
            {
                "word": " for",
                "start": 8.42,
                "end": 8.7
            },
            {
                "word": " his",
                "start": 8.7,
                "end": 8.98
            },
            {
                "word": " research.",
                "start": 8.98,
                "end": 9.6
            },
            {
                "word": " So",
                "start": 10.6,
                "end": 10.8
            },
            {
                "word": " far",
                "start": 10.8,
                "end": 11.02
            },
            {
                "word": " he",
                "start": 11.02,
                "end": 11.24
            },
            {
                "word": " kept",
                "start": 11.24,
                "end": 11.52
            },
            {
                "word": " gifting",
                "start": 11.52,
                "end": 12.02
            },
            {
                "word": " his",
                "start": 12.02,
                "end": 12.36
            },
            {
                "word": " inventions",
                "start": 12.36,
                "end": 12.9
            },
            {
                "word": " and",
                "start": 12.9,
                "end": 13.28
            },
            {
                "word": " discoveries",
                "start": 13.28,
                "end": 13.84
            },
            {
                "word": " to",
                "start": 13.84,
                "end": 14.12
            },
            {
                "word": " the",
                "start": 14.12,
                "end": 14.34
            },
            {
                "word": " patrons.",
                "start": 14.34,
                "end": 14.88
            },
            {
                "word": " But",
                "start": 15.7,
                "end": 16.0
            },
            {
                "word": " he",
                "start": 16.0,
                "end": 16.22
            },
            {
                "word": " had",
                "start": 16.22,
                "end": 16.4
            },
            {
                "word": " to",
                "start": 16.4,
                "end": 16.7
            },
            {
                "word": " depend",
                "start": 16.7,
                "end": 16.98
            },
            {
                "word": " on",
                "start": 16.98,
                "end": 17.18
            },
            {
                "word": " their",
                "start": 17.18,
                "end": 17.46
            },
            {
                "word": " generosity.",
                "start": 17.46,
                "end": 18.22
            },
            {
                "word": " He",
                "start": 18.76,
                "end": 19.04
            },
            {
                "word": " gifted",
                "start": 19.04,
                "end": 19.44
            },
            {
                "word": " his",
                "start": 19.44,
                "end": 19.8
            },
            {
                "word": " military",
                "start": 19.8,
                "end": 20.32
            },
            {
                "word": " compass",
                "start": 20.32,
                "end": 20.8
            },
            {
                "word": " to",
                "start": 20.8,
                "end": 21.04
            },
            {
                "word": " Duke",
                "start": 21.04,
                "end": 21.32
            },
            {
                "word": " of",
                "start": 21.32,
                "end": 21.58
            },
            {
                "word": " Gonzaga.",
                "start": 21.58,
                "end": 22.42
            },
            {
                "word": " In",
                "start": 22.68,
                "end": 22.96
            },
            {
                "word": " return",
                "start": 22.96,
                "end": 23.36
            },
            {
                "word": " most",
                "start": 23.36,
                "end": 23.76
            },
            {
                "word": " of",
                "start": 23.76,
                "end": 23.96
            },
            {
                "word": " the",
                "start": 23.96,
                "end": 24.18
            },
            {
                "word": " time",
                "start": 24.18,
                "end": 24.4
            },
            {
                "word": " he",
                "start": 24.4,
                "end": 24.66
            },
            {
                "word": " received",
                "start": 24.66,
                "end": 25.04
            },
            {
                "word": " gifts",
                "start": 25.04,
                "end": 25.48
            },
            {
                "word": " but",
                "start": 25.48,
                "end": 25.8
            },
            {
                "word": " not",
                "start": 25.8,
                "end": 26.12
            },
            {
                "word": " enough",
                "start": 26.12,
                "end": 26.48
            },
            {
                "word": " cash",
                "start": 26.48,
                "end": 26.78
            },
            {
                "word": " to",
                "start": 26.78,
                "end": 27.02
            },
            {
                "word": " further",
                "start": 27.02,
                "end": 27.36
            },
            {
                "word": " his",
                "start": 27.36,
                "end": 27.68
            },
            {
                "word": " research.",
                "start": 27.68,
                "end": 28.32
            },
            {
                "word": " In",
                "start": 29.18,
                "end": 29.38
            },
            {
                "word": " 1610",
                "start": 29.38,
                "end": 30.26
            },
            {
                "word": " he",
                "start": 30.26,
                "end": 30.46
            },
            {
                "word": " thought",
                "start": 30.46,
                "end": 30.8
            },
            {
                "word": " of",
                "start": 30.8,
                "end": 31.0
            },
            {
                "word": " a",
                "start": 31.0,
                "end": 31.2
            },
            {
                "word": " new",
                "start": 31.2,
                "end": 31.42
            },
            {
                "word": " strategy.",
                "start": 31.42,
                "end": 32.1
            },
            {
                "word": " He",
                "start": 32.6,
                "end": 32.82
            },
            {
                "word": " had",
                "start": 32.82,
                "end": 33.08
            },
            {
                "word": " recently",
                "start": 33.08,
                "end": 33.7
            },
            {
                "word": " discovered",
                "start": 33.7,
                "end": 34.26
            },
            {
                "word": " the",
                "start": 34.26,
                "end": 34.56
            },
            {
                "word": " moons",
                "start": 34.56,
                "end": 34.76
            },
            {
                "word": " of",
                "start": 34.76,
                "end": 35.02
            },
            {
                "word": " Jupiter.",
                "start": 35.02,
                "end": 35.54
            },
            {
                "word": " He",
                "start": 36.08,
                "end": 36.26
            },
            {
                "word": " was",
                "start": 36.26,
                "end": 36.58
            },
            {
                "word": " aware",
                "start": 36.58,
                "end": 36.86
            },
            {
                "word": " of",
                "start": 36.86,
                "end": 37.12
            },
            {
                "word": " the",
                "start": 37.12,
                "end": 37.32
            },
            {
                "word": " Medicis,",
                "start": 37.32,
                "end": 38.1
            },
            {
                "word": " who",
                "start": 38.6,
                "end": 38.8
            },
            {
                "word": " had",
                "start": 38.8,
                "end": 39.02
            },
            {
                "word": " Jupiter",
                "start": 39.02,
                "end": 39.54
            },
            {
                "word": " as",
                "start": 39.54,
                "end": 39.86
            },
            {
                "word": " their",
                "start": 39.86,
                "end": 40.04
            },
            {
                "word": " symbol",
                "start": 40.04,
                "end": 40.44
            },
            {
                "word": " in",
                "start": 40.44,
                "end": 40.68
            },
            {
                "word": " the",
                "start": 40.68,
                "end": 40.84
            },
            {
                "word": " 1540s.",
                "start": 40.84,
                "end": 42.26
            },
            {
                "word": " He",
                "start": 42.36,
                "end": 42.76
            },
            {
                "word": " announced",
                "start": 42.76,
                "end": 43.2
            },
            {
                "word": " that",
                "start": 43.2,
                "end": 43.4
            },
            {
                "word": " the",
                "start": 43.4,
                "end": 43.7
            },
            {
                "word": " bright",
                "start": 43.7,
                "end": 44.0
            },
            {
                "word": " stars,",
                "start": 44.0,
                "end": 44.58
            },
            {
                "word": " moons,",
                "start": 45.06,
                "end": 45.62
            },
            {
                "word": " appeared",
                "start": 46.24,
                "end": 46.52
            },
            {
                "word": " to",
                "start": 46.52,
                "end": 46.74
            },
            {
                "word": " him",
                "start": 46.74,
                "end": 46.96
            },
            {
                "word": " during",
                "start": 46.96,
                "end": 47.36
            },
            {
                "word": " the",
                "start": 47.36,
                "end": 47.66
            },
            {
                "word": " same",
                "start": 47.66,
                "end": 47.94
            },
            {
                "word": " time",
                "start": 47.94,
                "end": 48.24
            },
            {
                "word": " when",
                "start": 48.24,
                "end": 48.54
            },
            {
                "word": " Cosimo",
                "start": 48.54,
                "end": 49.04
            },
            {
                "word": " II",
                "start": 49.04,
                "end": 49.28
            },
            {
                "word": " was",
                "start": 49.28,
                "end": 49.66
            },
            {
                "word": " enthroned.",
                "start": 49.66,
                "end": 50.26
            },
            {
                "word": " He",
                "start": 51.04,
                "end": 51.28
            },
            {
                "word": " went",
                "start": 51.28,
                "end": 51.58
            },
            {
                "word": " on",
                "start": 51.58,
                "end": 51.8
            },
            {
                "word": " to",
                "start": 51.8,
                "end": 52.02
            },
            {
                "word": " mention",
                "start": 52.02,
                "end": 52.38
            },
            {
                "word": " the",
                "start": 52.38,
                "end": 52.62
            },
            {
                "word": " four",
                "start": 52.62,
                "end": 52.92
            },
            {
                "word": " moons",
                "start": 52.92,
                "end": 53.26
            },
            {
                "word": " around",
                "start": 53.26,
                "end": 53.68
            },
            {
                "word": " Jupiter",
                "start": 53.68,
                "end": 54.2
            },
            {
                "word": " resembled",
                "start": 54.2,
                "end": 54.92
            },
            {
                "word": " the",
                "start": 54.92,
                "end": 55.2
            },
            {
                "word": " four",
                "start": 55.2,
                "end": 55.46
            },
            {
                "word": " Medicis.",
                "start": 56.220000000000006,
                "end": 56.84
            },
            {
                "word": " Cosimo",
                "start": 57.12,
                "end": 57.66
            },
            {
                "word": " II",
                "start": 57.66,
                "end": 57.96
            },
            {
                "word": " and",
                "start": 57.96,
                "end": 58.22
            },
            {
                "word": " his",
                "start": 58.22,
                "end": 58.46
            },
            {
                "word": " siblings.",
                "start": 58.46,
                "end": 59.06
            },
            {
                "word": " Later",
                "start": 59.74,
                "end": 60.24
            },
            {
                "word": " Cosimo",
                "start": 60.24,
                "end": 61.06
            },
            {
                "word": " II",
                "start": 61.06,
                "end": 61.34
            },
            {
                "word": " made",
                "start": 61.34,
                "end": 61.62
            },
            {
                "word": " his",
                "start": 61.62,
                "end": 61.9
            },
            {
                "word": " official",
                "start": 61.9,
                "end": 62.38
            },
            {
                "word": " court",
                "start": 62.38,
                "end": 62.68
            },
            {
                "word": " philosopher",
                "start": 62.68,
                "end": 63.38
            },
            {
                "word": " and",
                "start": 63.38,
                "end": 63.78
            },
            {
                "word": " mathematician",
                "start": 63.78,
                "end": 64.5
            },
            {
                "word": " with",
                "start": 64.5,
                "end": 64.82
            },
            {
                "word": " a",
                "start": 64.82,
                "end": 65.0
            },
            {
                "word": " full",
                "start": 65.0,
                "end": 65.2
            },
            {
                "word": " salary.",
                "start": 65.2,
                "end": 65.8
            },
            {
                "word": " His",
                "start": 66.62,
                "end": 66.88
            },
            {
                "word": " days",
                "start": 66.88,
                "end": 67.16
            },
            {
                "word": " of",
                "start": 67.16,
                "end": 67.5
            },
            {
                "word": " begging",
                "start": 67.5,
                "end": 67.74
            },
            {
                "word": " and",
                "start": 67.74,
                "end": 68.08
            },
            {
                "word": " hoping",
                "start": 68.08,
                "end": 68.36
            },
            {
                "word": " for",
                "start": 68.36,
                "end": 68.72
            },
            {
                "word": " patronage",
                "start": 68.72,
                "end": 69.26
            },
            {
                "word": " were",
                "start": 69.26,
                "end": 69.54
            },
            {
                "word": " over",
                "start": 69.54,
                "end": 69.8
            },
            {
                "word": " with",
                "start": 69.8,
                "end": 70.04
            },
            {
                "word": " his",
                "start": 70.04,
                "end": 70.3
            },
            {
                "word": " master",
                "start": 70.3,
                "end": 70.74
            },
            {
                "word": " stroke.",
                "start": 70.74,
                "end": 71.26
            },
            {
                "word": " The",
                "start": 72.08,
                "end": 72.34
            },
            {
                "word": " lesson,",
                "start": 72.34,
                "end": 72.8
            },
            {
                "word": " every",
                "start": 73.08,
                "end": 73.48
            },
            {
                "word": " master",
                "start": 73.48,
                "end": 73.94
            },
            {
                "word": " would",
                "start": 73.94,
                "end": 74.24
            },
            {
                "word": " want",
                "start": 74.24,
                "end": 74.44
            },
            {
                "word": " to",
                "start": 74.44,
                "end": 74.72
            },
            {
                "word": " appear",
                "start": 74.72,
                "end": 74.94
            },
            {
                "word": " more",
                "start": 74.94,
                "end": 75.3
            },
            {
                "word": " brilliant.",
                "start": 75.3,
                "end": 75.82
            },
            {
                "word": " They",
                "start": 76.34,
                "end": 76.64
            },
            {
                "word": " all",
                "start": 76.64,
                "end": 76.9
            },
            {
                "word": " want",
                "start": 76.9,
                "end": 77.08
            },
            {
                "word": " to",
                "start": 77.08,
                "end": 77.42
            },
            {
                "word": " appear",
                "start": 77.42,
                "end": 77.66
            },
            {
                "word": " powerful",
                "start": 77.66,
                "end": 78.28
            },
            {
                "word": " and",
                "start": 78.28,
                "end": 78.58
            },
            {
                "word": " more",
                "start": 78.58,
                "end": 78.8
            },
            {
                "word": " important",
                "start": 78.8,
                "end": 79.4
            },
            {
                "word": " than",
                "start": 79.4,
                "end": 79.6
            },
            {
                "word": " the",
                "start": 79.6,
                "end": 79.88
            },
            {
                "word": " work",
                "start": 79.88,
                "end": 80.06
            },
            {
                "word": " produced",
                "start": 80.06,
                "end": 80.64
            },
            {
                "word": " in",
                "start": 80.64,
                "end": 80.92
            },
            {
                "word": " their",
                "start": 80.92,
                "end": 81.16
            },
            {
                "word": " name.",
                "start": 81.16,
                "end": 81.48
            },
            {
                "word": " By",
                "start": 82.16,
                "end": 82.52
            },
            {
                "word": " linking",
                "start": 82.52,
                "end": 82.92
            },
            {
                "word": " them",
                "start": 82.92,
                "end": 83.22
            },
            {
                "word": " with",
                "start": 83.22,
                "end": 83.54
            },
            {
                "word": " cosmic",
                "start": 83.54,
                "end": 84.0
            },
            {
                "word": " forces",
                "start": 84.0,
                "end": 84.52
            },
            {
                "word": " he",
                "start": 84.52,
                "end": 84.74
            },
            {
                "word": " made",
                "start": 84.74,
                "end": 84.98
            },
            {
                "word": " them",
                "start": 84.98,
                "end": 85.26
            },
            {
                "word": " shine",
                "start": 85.26,
                "end": 85.6
            },
            {
                "word": " brilliantly",
                "start": 85.6,
                "end": 86.34
            },
            {
                "word": " throughout",
                "start": 86.34,
                "end": 86.72
            },
            {
                "word": " the",
                "start": 86.72,
                "end": 87.0
            },
            {
                "word": " country.",
                "start": 87.0,
                "end": 87.5
            },
            {
                "word": " He",
                "start": 88.28,
                "end": 88.44
            },
            {
                "word": " did",
                "start": 88.44,
                "end": 88.76
            },
            {
                "word": " not",
                "start": 88.76,
                "end": 89.02
            },
            {
                "word": " outshine",
                "start": 89.02,
                "end": 89.58
            },
            {
                "word": " his",
                "start": 89.58,
                "end": 89.86
            },
            {
                "word": " master.",
                "start": 89.86,
                "end": 90.34
            },
            {
                "word": " He",
                "start": 90.86,
                "end": 91.08
            },
            {
                "word": " made",
                "start": 91.08,
                "end": 91.38
            },
            {
                "word": " his",
                "start": 91.38,
                "end": 91.68
            },
            {
                "word": " master",
                "start": 91.68,
                "end": 92.12
            },
            {
                "word": " outshine",
                "start": 92.12,
                "end": 92.82
            },
            {
                "word": " everyone.",
                "start": 92.82,
                "end": 93.4
            },
            {
                "word": " In",
                "start": 93.9,
                "end": 94.18
            },
            {
                "word": " the",
                "start": 94.18,
                "end": 94.4
            },
            {
                "word": " end",
                "start": 94.4,
                "end": 94.54
            },
            {
                "word": " he",
                "start": 94.54,
                "end": 94.84
            },
            {
                "word": " benefited",
                "start": 94.84,
                "end": 95.4
            },
            {
                "word": " from",
                "start": 95.4,
                "end": 95.74
            },
            {
                "word": " this",
                "start": 95.74,
                "end": 95.98
            },
            {
                "word": " as",
                "start": 95.98,
                "end": 96.34
            },
            {
                "word": " much",
                "start": 96.34,
                "end": 96.52
            },
            {
                "word": " he",
                "start": 96.52,
                "end": 96.74
            },
            {
                "word": " would",
                "start": 96.74,
                "end": 96.96
            },
            {
                "word": " have",
                "start": 96.96,
                "end": 97.1
            },
            {
                "word": " wanted.",
                "start": 97.1,
                "end": 97.6
            }
        ]
