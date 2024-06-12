import os
import time

from directory_creator import DirectoryCreator
from doc_reader import DocReader
from audio_generator import AudioGenerator
from image_generator import ImageGenerator
from video_generator import VideoGenerator
from uploader import Uploader


resources = ['audio', 'image', 'video']
jobs_dir = os.path.join(os.getcwd(), 'resources/jobs')

# Setting Open-AI access token in environment variable
os.environ["OPEN_API_ACCESS_TOKEN"] = "mock-api-key"

for job_file in os.listdir(jobs_dir):
    if job_file.endswith('.doc') or job_file.endswith('.docx'):
        job_id = job_file.split(".")[0]
        start_time = time.time()
        print("Starting job for " + job_id + ".............\n")

        # Step 1: Clean up existing job's assets
        directory_creator = DirectoryCreator(resources, jobs_dir)
        directories = directory_creator.create_resource_directories(job_id)

        # Step 2: Extract prompts and subtitles
        data = DocReader().read_doc(os.path.join(jobs_dir, job_file))

        # Step 3: Fetch and save images from Open AI
        image_generator = ImageGenerator(data.get("Prompts"), directories["image_dir"])
        image_generator.generate_and_save_images()

        # Step 4: Generate audio from subtitles
        audio_generator = AudioGenerator(data, directories['audio_dir'])
        audio_generator.generate_audio()
        audio_generator.get_subtitles_with_timestamp()

        # Step 5: Generate video from images and audio with subtitles
        video_generator = VideoGenerator(directories["image_dir"], directories["video_dir"], directories["audio_dir"],
                                         audio_generator.audio_runtime, audio_generator.image_screen_time,
                                         image_generator.prompts_and_images)
        video_generator.images_to_video()
        video_generator.add_subtitles_and_audio_to_video(audio_generator.subtitles_context)

        # Step 6: Upload file to GDrive
        uploader = Uploader(video_generator.video_name, job_id)
        uploader.upload()
        end_time = time.time()
        print("Job for " + job_id + " completed!! Time taken: " + str(end_time - start_time) + " seconds\n\n")
