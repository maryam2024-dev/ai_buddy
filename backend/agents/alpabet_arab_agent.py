from datetime import datetime
from pathlib import Path
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


router = APIRouter()

# Assuming Together client is already initialized
# client_together = Together(api_key=OPENAI_API_KEY_TOGETHER)
client = OpenAI(
	base_url="https://router.huggingface.co/novita",
#  base_url="https://router.huggingface.co/fireworks-ai",
	api_key=HUGGINGFACE_TOKEN
)

# Local directory for storing images
IMAGE_DIR = Path("generated_images")
IMAGE_DIR.mkdir(exist_ok=True)



# # Define the Hugging Face Inference API URL for the Mistral model
# API_URL = "https://router.huggingface.co/hf-inference/models/asafaya/bert-base-arabic"

# Set up headers with the API token
headers = {
    "Authorization": f"Bearer {HUGGINGFACE_TOKEN}",
    "Content-Type": "application/json"
}





# Local directory for storing images
IMAGE_DIR = Path("generated_images")
IMAGE_DIR.mkdir(exist_ok=True)

# Define the request model
class GenerateArabicRequest(BaseModel):
    level: int  # 1, 2, or 3

@router.post("/generate", status_code=201)
async def generate_arabic_alphabetic_image(request: GenerateArabicRequest):
    """
    Generate an Arabic alphabet learning exercise with an image.
    Level 1: Image + 3 words (1 correct, 2 incorrect)
    Level 2: List of 5 words + 5 letters (kids map them)
    Level 3: Word with a missing letter + Image hint + 3 choices (1 correct)
    """

    level = request.level

    # Define prompt based on level
    if level == 1:
        text_prompt = "اختر صورة لحيوان أو شيء معبر عن أحد الحروف الأبجدية العربية، ثم قم بإنشاء ثلاثة كلمات تحت الصورة، واحدة صحيحة واثنتان خاطئتان."
        image_prompt = "صورة لحيوان أو شيء يمثل أحد الحروف الأبجدية العربية بشكل واضح."
    elif level == 2:
        text_prompt = "قم بإنشاء قائمة تحتوي على 5 كلمات عربية وقائمة أخرى تحتوي على 5 أحرف، بحيث يتمكن الطفل من مطابقة كل كلمة بالحرف المناسب لها."
        image_prompt = "صورة تحتوي على 5 كلمات وأحرف لمطابقتها."
        text_prompt+=" make sure to not return any words with another language than arabic , make sure to not retun comment or explanation just the key value dict that map the two lists together"
        text_prompt+=" do not add the ال if the word does not contain it "

    elif level == 3:
        text_prompt = "اختر كلمة عربية تحتوي على حرف ناقص، مع توفير صورة تعبر عن هذه الكلمة، ثم قدم 3 خيارات للحرف المفقود، بحيث يكون أحدها صحيحًا والآخران خاطئان."
        image_prompt = "صورة لكلمة عربية تحتوي على حرف ناقص مع 3 اختيارات للحرف الصحيح."
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
        dalle_response = openai.Image.create(
            prompt=image_prompt,
            n=1,
            size="1024x1024"
        )
        image_url = dalle_response["data"][0]["url"]

        # Download and save the image locally
        image_filename = f"{uuid.uuid4()}.png"
        image_path = IMAGE_DIR / image_filename

        img_data = requests.get(image_url).content
        with open(image_path, "wb") as img_file:
            img_file.write(img_data)

        saved_image_url = f"/static/{image_filename}"  # Modify based on your static file setup

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"حدث خطأ أثناء توليد الصورة: {e}")

    return {
        "level": level,
        "exercise": text_content,
        "image_url": saved_image_url
    }

