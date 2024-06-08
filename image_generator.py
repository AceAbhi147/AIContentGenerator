import os
import openai
import requests
from PIL import Image
from io import BytesIO


# Set your OpenAI API Key
openai.api_key = "mock-api-key"


class ImageGenerator:
    def __init__(self, prompts, output_file_path, image_dimensions="1024x1024"):
        self.prompts = prompts
        self.output_file_path = output_file_path
        self.image_dimensions = image_dimensions

    def __pad_image(self, image, target_size=(1920, 1080)):
        target_width, target_height = target_size
        background = Image.new('RGB', target_size, (0, 0, 0))
        width, height = image.size
        position = ((target_width - width) // 2, (target_height - height) // 2)
        background.paste(image, position)
        return background

    # Function to generate an image using OpenAI
    def generate_and_save_images(self):
        count = 1
        for prompt in self.prompts:
            response = openai.images.generate(
                prompts=prompt,
                n=1,
                size=self.image_dimensions
            )
            image_url = response['data'][0]['url']

            # Get image from the URL and save it
            response = requests.get(image_url)
            img = Image.open(BytesIO(response.content))
            img = self.__pad_image(img)
            img.save(f'{self.output_file_path}/{count}.png')
            count += 1
            print("Image generated and saved at: " + self.output_file_path)

    def pad_all_existing_image(self, images_path=None):
        file_path = self.output_file_path
        if images_path:
            file_path = images_path

        if os.path.exists(file_path):
            count = 1
            for file in os.listdir(file_path):
                if file.endswith((".png", ".jpg", ".webp", ".jpeg")):
                    file_extension = file.split(".")[-1]
                    img = Image.open(os.path.join(file_path, file))
                    img = self.__pad_image(img)
                    img.save(f'{self.output_file_path}/{count}.{file_extension}')
                    count += 1
