import os
import json
import glob

from openai import OpenAI

import requests
from PIL import Image

AI_IMAGE_MODEL = 'dall-e-3'

def gen_image(task):
    folder_name = glob.escape(f"files/data/{task['group'].replace('/', ',')}")
    if not os.path.exists(folder_name):
        os.mkdir(folder_name)
    folder_name = glob.escape(f"{folder_name}/{task['name'].replace('/', ',')}")
    if not os.path.exists(folder_name):
        os.mkdir(folder_name)
    temp_image_file = f"{folder_name}/problem.webp"
    image_file_name = f"{folder_name}/problem.png"

    if not os.path.exists(temp_image_file) and not os.path.exists(image_file_name):
        client = OpenAI()
        image_prompt = task["description_image"]
        image_url = client.images.generate(
            model=AI_IMAGE_MODEL,
            prompt=image_prompt,
            size="1024x1024",
            quality="standard",
            n=1,
            
        ).data[0].url
        response = requests.get(image_url)
        with open(temp_image_file, 'wb') as f:
            f.write(response.content)
        
    if os.path.exists(temp_image_file) and not os.path.exists(image_file_name):
        webp_image = Image.open(temp_image_file)
        png_image = webp_image.convert("RGBA")
        png_image.save(image_file_name)

    temp_image_file = f"{folder_name}/solution.webp"
    image_file_name = f"{folder_name}/solution.png"

    if not os.path.exists(temp_image_file) and not os.path.exists(image_file_name):
        client = OpenAI()
        image_prompt = task["solution_image"]
        image_url = client.images.generate(
            model=AI_IMAGE_MODEL,
            prompt=image_prompt,
            size="1024x1024",
            quality="standard",
            n=1,
            
        ).data[0].url
        response = requests.get(image_url)
        with open(temp_image_file, 'wb') as f:
            f.write(response.content)
        
    if os.path.exists(temp_image_file) and not os.path.exists(image_file_name):
        webp_image = Image.open(temp_image_file)
        png_image = webp_image.convert("RGBA")
        png_image.save(image_file_name)


def gen(count):
    tasks = json.load(open('files/in_progress.json', 'rt', encoding='UTF-8'))
    for i, task in enumerate(tasks):
        if i < count:
            gen_image(task)
            
if __name__ == '__main__':
    gen(1)