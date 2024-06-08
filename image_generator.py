import openai
import requests
from PIL import Image
from io import BytesIO


# Set your OpenAI API Key
openai.api_key = "mock-api"


class ImageGenerator:
    # Function to generate an image using OpenAI
    def generate_and_save_images(self, prompts, output_file_path, job_id):
        count = 1
        for prompt in prompts:
            response = openai.images.generate(
                prompts=prompts,
                n=1,
                size="1024x1024"
            )
            image_url = response['data'][0]['url']

            # Get image from the URL and save it
            response = requests.get(image_url)
            img = Image.open(BytesIO(response.content))
            img.save(f'{output_file_path}/{job_id}/{count}.png')
            count += 1
            print("Image generated and saved at: " + output_file_path)
