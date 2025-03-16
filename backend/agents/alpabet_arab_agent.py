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

from fastapi import APIRouter, HTTPException
import requests


router = APIRouter()

# Assuming Together client is already initialized
# client_together = Together(api_key=OPENAI_API_KEY_TOGETHER)
client = OpenAI(
	# base_url="https://router.huggingface.co/novita",
	api_key=OPENAI_API_KEY
)

# Local directory for storing images
IMAGE_DIR = Path("generated_images")
IMAGE_DIR.mkdir(exist_ok=True)



# # Define the Hugging Face Inference API URL for the Mistral model
# API_URL = "https://router.huggingface.co/hf-inference/models/asafaya/bert-base-arabic"

# # Set up headers with the API token
# headers = {
#     "Authorization": f"Bearer {HUGGINGFACE_TOKEN}",
#     "Content-Type": "application/json"
# }


from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import openai
import requests
import uuid
from pathlib import Path
from utils.load_helper import OPENAI_API_KEY_TOGETHER,HUGGINGFACE_TOKEN,OPENAI_API_KEY



# # Define API Keys
# OPENAI_API_KEY = "your_openai_api_key"

# Local directory for storing images
IMAGE_DIR = Path("generated_images")
IMAGE_DIR.mkdir(exist_ok=True)

# Define the request model
class GenerateArabicRequest(BaseModel):
    level: int  # 1, 2, or 3

@router.post("/generate_arabic", status_code=201)
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
    elif level == 3:
        text_prompt = "اختر كلمة عربية تحتوي على حرف ناقص، مع توفير صورة تعبر عن هذه الكلمة، ثم قدم 3 خيارات للحرف المفقود، بحيث يكون أحدها صحيحًا والآخران خاطئان."
        image_prompt = "صورة لكلمة عربية تحتوي على حرف ناقص مع 3 اختيارات للحرف الصحيح."
    else:
        raise HTTPException(status_code=400, detail="المستوى غير صحيح. اختر مستوى بين 1 و 3.")

    # Generate text content
    try:
    #     response = client.chat.completions.create(
    #     # model="Qwen/Qwen2.5-Coder-32B-Instruct",
    #     # meta-llama-llama-2-70b-hf
    # #    model="Meta-Llama-3.3-70B-Instruct",
    # # model="meta-llama/Llama-2-70b-chat-hf",
    # # model="mistralai/Mistral-7B-Instruct-v0.1",
    # model="meta-llama/llama-3-70b-instruct",
    #     messages=[{"role": "user", "content": text_prompt}],
    # )
        # text_content = response["choices"][0]["message"]["content"].strip()
        # # Extract the generated story from the response
        # if hasattr(response, "choices") and response.choices:
        #     first_choice = response.choices[0]

        #     if hasattr(first_choice, "message") and hasattr(first_choice.message, "content"):
        #         text_content = first_choice.message.content.strip()
        #         print(f"text_content: {text_content}")
        response = openai.ChatCompletion.create(
            model="gpt-4-turbo",
            messages=[{"role": "user", "content": text_prompt}]
        )
        text_content = response["choices"][0]["message"]["content"].strip()
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



# class GenerateArabicRequest(BaseModel):
#     level: int  # 1, 2, or 3

# @router.post("/generate_arabic", status_code=201)
# async def generate_arabic_alphabetic_image(request: GenerateArabicRequest):
#     """
#     Generate an Arabic alphabet learning exercise based on the given level.
#     Level 1: Image of an object (e.g., elephant) + 3 words (1 correct, 2 incorrect)
#     Level 2: List of 5 words + 5 letters (kids map them)
#     Level 3: Word with a missing letter + Image hint + 3 possible answers (1 correct)
#     """

#     level = request.level

#     # Define the prompt based on level
#     if level == 1:
#         prompt = (
#             "اختر صورة لحيوان أو شيء معبر عن أحد الحروف الأبجدية العربية، "
#             "ثم قم بإنشاء ثلاثة كلمات تحت الصورة، واحدة صحيحة واثنتان خاطئتان."
#         )
#     elif level == 2:
#         prompt = (
#             "قم بإنشاء قائمة تحتوي على 5 كلمات عربية وقائمة أخرى تحتوي على 5 أحرف، "
#             "بحيث يتمكن الطفل من مطابقة كل كلمة بالحرف المناسب لها."
#         )
#     elif level == 3:
#         prompt = (
#             "اختر كلمة عربية تحتوي على حرف ناقص، مع توفير صورة تعبر عن هذه الكلمة، "
#             "ثم قدم 3 خيارات للحرف المفقود، بحيث يكون أحدها صحيحًا والآخران خاطئان."
#         )
#     else:
#         raise HTTPException(status_code=400, detail="المستوى غير صحيح. اختر مستوى بين 1 و 3.")


#     # print(f"full_prompt: {full_prompt}")

#     # Call the AI model to generate the story
#     response = client.chat.completions.create(
#         model="Qwen/Qwen2.5-Coder-32B-Instruct",
#         # meta-llama-llama-2-70b-hf
#     #    model="Meta-Llama-3.3-70B-Instruct",
#     # model="meta-llama/Llama-2-70b-chat-hf",
#     # model="mistralai/Mistral-7B-Instruct-v0.1",
#     # model="meta-llama/llama-3-70b-instruct",
#         messages=[{"role": "user", "content": prompt}],
#     )

#     try:
#         print("before api model....")
#         print(f"ai_response: {response}")

#         # Extract the generated story from the response
#         if hasattr(response, "choices") and response.choices:
#             first_choice = response.choices[0]

#             if hasattr(first_choice, "message") and hasattr(first_choice.message, "content"):
#                 story_content = first_choice.message.content.strip()
#                 print(f"story_content: {story_content}")

#                 # Return the generated story
#                 return {"story": story_content}

#         raise HTTPException(status_code=400, detail="Failed to extract story content from AI response.")
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=f"Failed to generate or parse AI response: {e}")
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
#                 "max_length": 500,  # Adjust the maximum length as needed
#                 "num_return_sequences": 1,
#                 "temperature": 0.7,
#                 "do_sample": True
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