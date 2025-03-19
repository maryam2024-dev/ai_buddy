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
API_URL = "https://router.huggingface.co/hf-inference/models/asafaya/bert-base-arabic"


# Set up headers with the API token
headers = {
    "Authorization": f"Bearer {HUGGINGFACE_TOKEN}",
    "Content-Type": "application/json"
}



router = APIRouter()

# Directory to save images locally
IMAGE_SAVE_DIR = "storytelling_images"
os.makedirs(IMAGE_SAVE_DIR, exist_ok=True)

# Gradio Client Initialization
GRADIO_MODEL = "stabilityai/stable-diffusion-3-medium"


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
        response = hf_client.chat.completions.create(
            model="meta-llama/llama-3-70b-instruct",
            messages=[{"role": "user", "content": full_prompt}],
        )
        
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
        image_prompt = f"A colorful, dreamy children's illustration for a story about {text_content}, conveying the theme of {category} in the whimsical and magical style of Beatrice Blue. Soft painterly textures, fantasy elements, and warm pastel colors."

      
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
        image_path = os.path.join(IMAGE_SAVE_DIR, image_filename)
        
        # Copy the image from the Gradio-provided path to your local directory
        shutil.copy(gradio_image_path, image_path)
        print(f"Image copied to: {image_path}")

        # Construct the public URL for the image
        public_image_url = f"http://127.0.0.1:8000/{image_path}"
        print(f"Public image URL: {public_image_url}")
        

      
        # image_data = requests.get(result).content
        # with open(image_path, "wb") as f:
        #     f.write(image_data)
        
        # else:
        #     raise HTTPException(status_code=400, detail="Generated image not found.")

        

        # Step 4: Return the story and the path to the saved image
        return {
            "story": text_content,
            "image_path": public_image_url
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to generate or parse AI response: {e}")

# @router.post("/generate", status_code=201)
# async def create_user_stories(category: str, size: str):
#     """
#     Generate an English moral story for kids based on the provided category and size.

#     Parameters:
#         category (str): The moral value or theme of the story (e.g., "Honesty", "Cooperation").
#         size (str): The size of the story ("Short", "Medium", "Long").

#     Returns:
#         dict: A dictionary containing the generated story.
#     """
#     # Define size descriptions for clarity
#     size_descriptions = {
#         "Short": "A short story consisting of a single paragraph.",
#         "Medium": "A medium-length story consisting of several paragraphs.",
#         "Long": "A long story with details and multiple characters."
#     }

#     # Validate size input
#     if size not in size_descriptions:
#         raise HTTPException(status_code=400, detail="Invalid size. Please choose from 'Short', 'Medium', or 'Long'.")

#     # Construct the full prompt in English
#     full_prompt = (
#         f"Write a moral story in English for children about the theme of {category}. "
#         f"The story should be {size_descriptions[size]} and should teach children the value of {category}."
#     )

#     print(f"full_prompt: {full_prompt}")

#     try:
        
     
#         response = client.chat.completions.create(
#         # model="Qwen/Qwen2.5-Coder-32B-Instruct",
#         # meta-llama-llama-2-70b-hf
#         #    model="Meta-Llama-3.3-70B-Instruct",
#         # model="meta-llama/Llama-2-70b-chat-hf",
#         # model="mistralai/Mistral-7B-Instruct-v0.1",
#         model="meta-llama/llama-3-70b-instruct",
#             messages=[{"role": "user", "content": full_prompt}],
#         )
#         # Extract the generated story from the response
#         if hasattr(response, "choices") and response.choices:
#             first_choice = response.choices[0]

#             if hasattr(first_choice, "message") and hasattr(first_choice.message, "content"):
#                 text_content = first_choice.message.content.strip()
#                 print(f"text_content: {text_content}")
#                 return {"story": text_content}
        

#         raise HTTPException(status_code=400, detail="Unexpected response format from Hugging Face API.")
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=f"Failed to generate or parse AI response: {e}")



# from fastapi import APIRouter, HTTPException
# import requests



# # Define the Hugging Face Inference API URL for the CAMeL Lab Arabic GPT model
# API_URL = "https://api-inference.huggingface.co/models/CAMeL-Lab/bert-base-arabic-camelbert-ca"
# # Set up headers with the API token
# headers = {
#     "Authorization": f"Bearer {HUGGINGFACE_TOKEN}",
#     "Content-Type": "application/json"
# }

# @router.post("/generate", status_code=201)
# async def create_user_stories(category: str, size: str):
#     """
#     Generate an Arabic moral story for kids based on the provided category and size.

#     Parameters:
#         category (str): The moral value or theme of the story (e.g., "الصدق", "التعاون").
#         size (str): The size of the story ("قصير", "متوسط", "طويل").

#     Returns:
#         dict: A dictionary containing the generated story.
#     """
#     # Define size descriptions for clarity
#     size_descriptions = {
#         "قصير": "قصة قصيرة تتكون من فقرة واحدة فقط.",
#         "متوسط": "قصة متوسطة الطول تتكون من عدة فقرات.",
#         "طويل": "قصة طويلة تحتوي على تفاصيل وشخصيات متعددة."
#     }

#     # Validate size input
#     if size not in size_descriptions:
#         raise HTTPException(status_code=400, detail="Invalid size. Please choose from 'قصير', 'متوسط', or 'طويل'.")

#     # Construct the full prompt in Arabic
#     full_prompt = (
#         f"اكتب قصة أخلاقية باللغة العربية للأطفال حول موضوع {category}. "
#         f"يجب أن تكون القصة {size_descriptions[size]} وتُعلم الأطفال قيمة {category}."
#     )

#     print(f"full_prompt: {full_prompt}")

#     try:
#         # Prepare the payload for the API request
#         payload = {
#             "inputs": full_prompt,
#             "parameters": {
#                 # "max_length": 500,  # Adjust the maximum length as needed
#                 # "num_return_sequences": 1,
#                 # "no_repeat_ngram_size": 2,
#                 # "top_p": 0.95,
#                 # "temperature": 0.7,
#                 # "do_sample": True
#             }
#         }

#         # Send the request to the Hugging Face Inference API
#         response = requests.post(API_URL, headers=headers, json=payload)
        
#         print("before api model....")
#         print(f"ai_response: {response}")
#         print(f"ai_response: {response.json()}")
#         print(f"ai_response: {response.text}")
#         print(f"ai_response: {response.status_code}")


#         # Check if the request was successful
#         if response.status_code != 200:
#             raise HTTPException(status_code=response.status_code, detail=f"Failed to generate story: {response.text}")

#         # Parse the response
#         result = response.json()
#         if isinstance(result, list) and len(result) > 0:
#             story_content = result[0].get("generated_text", "").strip()
#             print(f"story_content: {story_content}")
#             return {"story": story_content}

#         raise HTTPException(status_code=400, detail="Unexpected response format from Hugging Face API.")
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=f"Failed to generate or parse AI response: {e}")