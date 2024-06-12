import os
import openai
import requests
from PIL import Image
from io import BytesIO


class ImageGenerator:
    def __init__(self, prompts_and_images, output_file_path, image_dimensions="1024x1024"):
        self.prompts_and_images = prompts_and_images
        self.output_file_path = output_file_path
        self.image_dimensions = image_dimensions

    def __resize_image(self, image, target_size=(720, 1280)):
        original_width, original_height = image.size
        aspect_ratio = original_width / original_height

        # Calculate new dimensions to fit within the background size
        target_width, target_height = target_size
        if aspect_ratio > 1:  # Image is wider than it is tall
            new_width = target_width
            new_height = int(target_width / aspect_ratio)
        else:  # Image is taller than it is wide
            new_height = target_height
            new_width = int(target_height * aspect_ratio)

        # Ensure the new dimensions fit within the background size
        if new_width > target_width:
            new_width = target_width
            new_height = int(new_width / aspect_ratio)
        if new_height > target_height:
            new_height = target_height
            new_width = int(new_height * aspect_ratio)

        # Resize the image
        return image.resize((new_width, new_height))

    def __pad_image(self, image, target_size=(720, 1280), bottom_padding=100):
        image = self.__resize_image(image, target_size)
        width, height = image.size
        target_width, target_height = target_size
        new_target_height = target_height - bottom_padding
        background = Image.new('RGB', (target_width, target_height), (0, 0, 0))
        position = ((target_width - width) // 2, (new_target_height - height) // 2)
        background.paste(image, position)
        return background

    # Function to generate an image using OpenAI
    def generate_and_save_images(self):
        print("Generating Images using extracted data.....................")
        for prompt_and_image in self.prompts_and_images:
            prompt = prompt_and_image[0]
            image_file = prompt_and_image[1]

            # Use OpenAI API Key from env properties
            openai.api_key = os.environ["OPEN_API_ACCESS_TOKEN"]

            response = openai.images.generate(
                model="dall-e-3",
                prompt=prompt,
                n=1,
                size=self.image_dimensions,
                quality="hd"
            )
            image_url = response.data[0].url

            # Get image from the URL and save it
            response = requests.get(image_url)
            img = Image.open(BytesIO(response.content))
            img = self.__pad_image(img)
            img.save(f'{self.output_file_path}/{image_file}')
        print("Images generated and saved at: " + self.output_file_path + "!!\n\n")

    def pad_all_existing_image(self, images_path=None):
        file_path = self.output_file_path
        if images_path:
            file_path = images_path
        print("Padding images present in " + str(file_path) + "........................")

        if os.path.exists(file_path):
            count = 1
            for file in os.listdir(file_path):
                if file.endswith((".png", ".jpg", ".webp", ".jpeg")):
                    file_extension = file.split(".")[-1]
                    img = Image.open(os.path.join(file_path, file))
                    img = self.__pad_image(img)
                    img.save(f'{self.output_file_path}/{count}.{file_extension}')
                    count += 1

        print("Images Padded and saved in: " + str(self.output_file_path) + "\n\n")
