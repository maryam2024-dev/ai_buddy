from datetime import datetime
import os
from pathlib import Path
import shutil
from fastapi import APIRouter, Body, Depends, HTTPException, Header, Query, status
from fastapi.responses import JSONResponse
from pymongo import MongoClient, ReturnDocument
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi import FastAPI, HTTPException, Depends, Header, status, Request
from pydantic import BaseModel, Field
from typing import List, Optional
from together import Together
from utils.load_helper import OPENAI_API_KEY_TOGETHER,HUGGINGFACE_TOKEN,OPENAI_API_KEY
from openai import OpenAI
import requests
from pydantic import BaseModel
import openai
import uuid
from gradio_client import Client





router = APIRouter()

# Assuming Together client is already initialized
# client_together = Together(api_key=OPENAI_API_KEY_TOGETHER)
client = OpenAI(
	base_url="https://router.huggingface.co/novita",
#  base_url="https://router.huggingface.co/fireworks-ai",
	api_key=HUGGINGFACE_TOKEN
)

# Local directory for storing images
IMAGE_DIR = Path("english_alph_learning_images")
IMAGE_DIR.mkdir(exist_ok=True)

# Gradio Client Initialization
GRADIO_MODEL = "stabilityai/stable-diffusion-3-medium"

# # Define the Hugging Face Inference API URL for the Mistral model
# API_URL = "https://router.huggingface.co/hf-inference/models/asafaya/bert-base-arabic"

# Set up headers with the API token
headers = {
    "Authorization": f"Bearer {HUGGINGFACE_TOKEN}",
    "Content-Type": "application/json"
}





# Define the request model
class GenerateArabicRequest(BaseModel):
    level: int  # 1, 2, or 3

@router.post("/generate", status_code=201)
async def generate_arabic_alphabetic_image(request: GenerateArabicRequest):
    level = request.level

# Define prompt based on level
    """
Generate an English alphabet learning exercise.
Four levels, each focusing on a specific type of question:
- Level 1: Match words to their starting letters (easiest, text-only)
- Level 2: Complete the missing letter in a word (text-only)
- Level 3: Explain the image in one word (image-based)
- Level 4: Say with which letter the image starts (hardest, image-based)

General Rules:
- Ensure all words and letters are in English.
- Use clear and recognizable images for image-based levels.
- Provide 3 choices for all multiple-choice questions (1 correct, 2 incorrect).
- Avoid adding unnecessary articles (e.g., 'the', 'a') unless they are part of the word.
- Use simple, kid-friendly words for all levels.
- Do not include any comments or explanations in the output, just the required elements.
"""

    level = request.level

# Define prompt based on level
    if level == 1:
        # Level 1: Match words to their starting letters (easiest, text-only)
        text_prompt = "Create a list of 3 simple English words (e.g., 'cat', 'ball', 'apple') and 3 letters (e.g., 'C', 'B', 'A'). The child should match each word to its correct starting letter."
        image_prompt = None  # No image needed for this level

    elif level == 2:
        # Level 2: Complete the missing letter in a word (text-only)
        text_prompt = "Provide 3 simple English words (e.g., 'd_g', 'b_x', 's_n'), each with one missing letter. Include 3 letter choices for each word (1 correct, 2 incorrect). The child should choose the correct letter to complete the word."
        image_prompt = None  # No image needed for this level

    elif level == 3:
        # Level 3: Explain the image in one word (image-based)
        text_prompt = "Show an image of an object or action (e.g., a dog, a car, a tree). Provide 3 simple word choices (1 correct, 2 incorrect) that describe the image. The child should choose the correct word."
        image_prompt = "An image of an object or action, clearly representing one simple word. Include the 3 word choices below the image."

    elif level == 4:
        # Level 4: Say with which letter the image starts (hardest, image-based)
        text_prompt = "Show an image of an object or action (e.g., a fish, a house, a kite). Provide 3 letter choices (1 correct, 2 incorrect) for the starting letter of the word represented by the image. The child should choose the correct letter."
        image_prompt = "An image of an object or action, clearly representing one simple word. Include the 3 letter choices below the image."
    else:
        raise HTTPException(status_code=400, detail="المستوى غير صحيح. اختر مستوى بين 1 و 3.")
    

    # Generate text content
    try:
        response = client.chat.completions.create(
        # model="Qwen/Qwen2.5-Coder-32B-Instruct",
        # meta-llama-llama-2-70b-hf
    #    model="Meta-Llama-3.3-70B-Instruct",
    # model="meta-llama/Llama-2-70b-chat-hf",
    # model="mistralai/Mistral-7B-Instruct-v0.1",
    model="meta-llama/llama-3-70b-instruct",
        messages=[{"role": "user", "content": text_prompt}],
    )
    
        # Extract the generated story from the response
        if hasattr(response, "choices") and response.choices:
            first_choice = response.choices[0]

            if hasattr(first_choice, "message") and hasattr(first_choice.message, "content"):
                text_content = first_choice.message.content.strip()
                print(f"text_content: {text_content}")
                if level == 2:
                    return {"level": level, "exercise": text_content}


    except Exception as e:
        raise HTTPException(status_code=500, detail=f"حدث خطأ أثناء توليد النص: {e}")

    # Generate image using OpenAI DALL·E
    try:
         # Step 1: Generate an image prompt based on the story
        image_prompt = f""

      
        # Define panorama dimensions
        panorama_width = 1536  # Wide width for panorama effect
        panorama_height = 512  # Standard height
       

        # prompt = "1girl, green hair, sweater, looking at viewer, upper body, beanie, outdoors, night, turtleneck, masterpiece, best quality"
         
        print("Connecting to Gradio client...")
        client_gradio = Client(GRADIO_MODEL)

        print(f"Generating image for prompt: {image_prompt}")
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
            raise HTTPException(status_code=400, detail="Invalid image result received.")

        

        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        image_filename = f"gradio_{timestamp}.png"
        image_path = os.path.join(IMAGE_DIR, image_filename)
        
        # Copy the image from the Gradio-provided path to your local directory
        shutil.copy(gradio_image_path, image_path)
        print(f"Image copied to: {image_path}")

        # Construct the public URL for the image
        public_image_url = f"http://127.0.0.1:8000/{image_path}"
        print(f"Public image URL: {public_image_url}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"حدث خطأ أثناء توليد الصورة: {e}")

    return {
        "level": level,
        "exercise": text_content,
        "image_url": public_image_url
    }

