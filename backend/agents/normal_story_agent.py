from datetime import datetime
import shutil
from fastapi.responses import JSONResponse
from pymongo import MongoClient, ReturnDocument
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi import FastAPI, HTTPException, Depends, Header, status, Request,APIRouter,Body,Query,status
from pydantic import BaseModel, Field
from typing import List, Optional
from together import Together
from utils.load_helper import OPENAI_API_KEY_TOGETHER,HUGGINGFACE_TOKEN,OPENAI_API_KEY
from openai import OpenAI
import requests
from diffusers import DiffusionPipeline
from PIL import Image
import requests
import os
from gradio_client import Client





router = APIRouter()


# Assuming Together client is already initialized
# client_together = Together(api_key=OPENAI_API_KEY_TOGETHER)
# Initialize Hugging Face client
hf_client = OpenAI(
    base_url="https://router.huggingface.co/novita",
    api_key=HUGGINGFACE_TOKEN
)



# Define the Hugging Face Inference API URL for the Mistral model
# API_URL = "https://router.huggingface.co/hf-inference/models/asafaya/bert-base-arabic"


# Set up headers with the API token
headers = {
    "Authorization": f"Bearer {HUGGINGFACE_TOKEN}",
    "Content-Type": "application/json"
}



router = APIRouter()

# Directory to save images locally
IMAGE_SAVE_DIR = "static/storytelling_images"
os.makedirs(IMAGE_SAVE_DIR, exist_ok=True)




# Gradio Client Initialization
GRADIO_MODEL = "stabilityai/stable-diffusion-3-medium"
GRADIO_MODEL="agents-course/text-to-image"


@router.post("/generate", status_code=201)
async def create_user_stories(category: str, size: str):
    """
    Generate an English moral story for kids based on the provided category and size,
    and generate an accompanying image saved locally.

    Parameters:
        category (str): The moral value or theme of the story (e.g., "Honesty", "Cooperation").
        size (str): The size of the story ("Short", "Medium", "Long").

    Returns:
        dict: A dictionary containing the generated story and the path to the saved image.
    """
    # Define size descriptions for clarity
    size_descriptions = {
        "Short": "A short story consisting of a single paragraph.",
        "Medium": "A medium-length story consisting of several paragraphs.",
        "Long": "A long story with details and multiple characters."
    }

    # Validate size input
    if size not in size_descriptions:
        raise HTTPException(status_code=400, detail="Invalid size. Please choose from 'Short', 'Medium', or 'Long'.")

    # Construct the full prompt in English
    full_prompt = (
        f"Write a moral story in English for children about the theme of {category}. "
        f"The story should be {size_descriptions[size]} and should teach children the value of {category}."
    )

    print(f"full_prompt: {full_prompt}")

    try:
        # Generate the story using the language model
        # response = hf_client.chat.completions.create(
        #     model="meta-llama/llama-3-70b-instruct",
        #     messages=[{"role": "user", "content": full_prompt}],
        # )
        client = Client("Qwen/Qwen2-72B-Instruct")
        
        

        client = Client("Rijgersberg/Qwen2.5-7B-Instruct")
        response = client.predict(
                prompt=full_prompt,
                api_name="/chat"
)

        # response = client.predict(
        #         query=full_prompt,
        #         history=[],
        #         system="You are a writer for children stories.",
        #         api_name="/model_chat"
        # )
        # text_content = response
        # Extract the generated story from the response
        if hasattr(response, "choices") and response.choices:
            first_choice = response.choices[0]

            if hasattr(first_choice, "message") and hasattr(first_choice.message, "content"):
                text_content = first_choice.message.content.strip()
                print(f"text_content: {text_content}")
            else:
                raise HTTPException(status_code=400, detail="Unexpected response format from Hugging Face API.")
        else:
            raise HTTPException(status_code=400, detail="No response choices found from Hugging Face API.")
        
        # Step 1: Generate an image prompt based on the story
        image_prompt = f"A vibrant, dreamy children's illustration that captures the essence of a story about {text_content}, visually depicting the theme of {category} with soft painterly textures, realistic yet whimsical characters, and warm pastel colors. The scene should be expressive, alive, and emotionally engaging, ensuring all elements—characters, objects, and environment—are accurate, well-proportioned, and fitting to the story. Avoid unrealistic distortions or irrelevant elements, embracing a charming and magical style inspired by Beatrice Blue."


      
        # Define panorama dimensions
        panorama_width = 1536  # Wide width for panorama effect
        panorama_height = 512  # Standard height
       

        # prompt = "1girl, green hair, sweater, looking at viewer, upper body, beanie, outdoors, night, turtleneck, masterpiece, best quality"
         
        print("Connecting to Gradio client...")
        client_gradio = Client(GRADIO_MODEL)
        # client = Client("agents-course/text-to-image")

        print(f"Generating image for prompt: {image_prompt}")
        
        
        # result = client.predict(
        #         param_0=image_prompt,
        #         api_name="/predict"
        # )
        # print(result)
        result = client_gradio.predict(
            prompt=image_prompt,
            negative_prompt="",
            seed=0,
            randomize_seed=True,
            width=panorama_width,
            height=panorama_height,
            guidance_scale=7.5,
            num_inference_steps=25,
            api_name="/infer"
        )

        print(f"Result from Gradio Client: {result}")  # Debugging line

        # Extract and validate the image path or URL
        
         # Extract the file path from the result
        if isinstance(result, (list, tuple)) and len(result) > 0:
            gradio_image_path = result[0]  # First element is the file path
        else:
            gradio_image_path = result
            # raise HTTPException(status_code=400, detail="Invalid image result received.")

        

        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        image_filename = f"gradio_{timestamp}.png"
        image_path = os.path.join(IMAGE_SAVE_DIR, image_filename)
        
        # Copy the image from the Gradio-provided path to your local directory
        shutil.copy(gradio_image_path, image_path)
        print(f"Image copied to: {image_path}")

        # Construct the public URL for the image
        public_image_url = f"http://127.0.0.1:8000/{image_path}"
        print(f"Public image URL: {public_image_url}")
        
        return {
            "story": text_content,
            "image_path": public_image_url
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to generate or parse AI response: {e}")


