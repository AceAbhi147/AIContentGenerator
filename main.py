import os
from directory_creator import DirectoryCreator
from doc_reader import DocReader
from audio_generator import AudioGenerator
from image_generator import ImageGenerator
from video_generator import VideoGenerator


resources = ['audio', 'image', 'video']
jobs_dir = os.path.join(os.getcwd(), 'resources/jobs')

for job_file in os.listdir(jobs_dir):
    if job_file.endswith('.doc') or job_file.endswith('.docx'):
        job_id = job_file.split(".")[0]

        directory_creator = DirectoryCreator(resources, jobs_dir)
        directories = directory_creator.create_resource_directories(job_id)

        # Step 1: Extract prompts and subtitles
        # data = DocReader().read_doc(os.path.join(jobs_dir, job_file))

        # # Step 2: Fetch and save images from Open AI
        # ImageGenerator().generate_and_save_images(prompts_and_subtitles["prompts"], config["image_folder"], job_id)

        # Step 3: Generate audio from subtitles
        # AudioGenerator().generate_audio(data, directories['audio_dir'])

        # Step 4: Generate video from images and audio with subtitles
        video_generator = VideoGenerator(directories["image_dir"], directories["video_dir"], directories["audio_dir"])
        video_generator.images_to_video()

        # Step 5: Combine Video and Audio
        video_generator.combine_audio_and_video()


