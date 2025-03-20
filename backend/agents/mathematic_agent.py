from datetime import datetime
# from fastapi import APIRouter, Body, Depends, HTTPException, Header, Query, status
# from fastapi.responses import JSONResponse
# from pymongo import MongoClient, ReturnDocument
# from motor.motor_asyncio import AsyncIOMotorClient
# from fastapi import FastAPI, HTTPException, Depends, Header, status, Request
from pydantic import BaseModel, Field
from typing import List, Optional

from together import Together

from utils.load_helper import OPENAI_API_KEY_TOGETHER, HUGGINGFACE_TOKEN, OPENAI_API_KEY
from openai import OpenAI

from fastapi import APIRouter, HTTPException
import requests

router = APIRouter()

# Assuming Together client is already initialized
client_together = Together(api_key=OPENAI_API_KEY_TOGETHER)
client = OpenAI(
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

# Define the request model
class GenerateMathRequest(BaseModel):
    level: int = Field(..., description="The difficulty level of the math question. Choose 1, 2, 3, or 4.")

@router.post("/generate-math", status_code=201)
async def generate_math_questions(request: GenerateMathRequest):
    """
    Generate math questions for kids with four levels in Arabic.
    Level 1: Simple addition (e.g., "ما هو ناتج ٢ + ٣؟")
    Level 2: Simple subtraction (e.g., "ما هو ناتج ٥ - ٢؟")
    Level 3: Counting objects (e.g., "إذا كان لديك ٣ تفاحات وأعطيت ١، كم تبقى لديك؟")
    Level 4: Comparison (e.g., "أيهما أكبر: ٥ أم ٣؟")
    """

    level = request.level

    # Define prompt based on level
    if level == 1:
        text_prompt = "أنشئ مسألة جمع بسيطة للأطفال بالأرقام العربية مع 3 خيارات للإجابة. مثال: 'ما هو ناتج ٢ + ٣؟ أ) ٥ ب) ٦ ج) ٧'"
    elif level == 2:
        text_prompt = "أنشئ مسألة طرح بسيطة للأطفال بالأرقام العربية مع 3 خيارات للإجابة. مثال: 'ما هو ناتج ٥ - ٢؟ أ) ٢ ب) ٣ ج) ٤'"
    elif level == 3:
        text_prompt = "أنشئ مسألة عد بسيطة للأطفال بالأرقام العربية مع 3 خيارات للإجابة. مثال: 'إذا كان لديك ٣ تفاحات وأعطيت ١، كم تبقى لديك؟ أ) ١ ب) ٢ ج) ٣'"
    elif level == 4:
        text_prompt = "أنشئ مسألة مقارنة بسيطة للأطفال بالأرقام العربية مع 3 خيارات للإجابة. مثال: 'أيهما أكبر: ٥ أم ٣؟ أ) ٥ ب) ٣ ج) ٤'"
    else:
        raise HTTPException(status_code=400, detail="المستوى غير صحيح. اختر مستوى بين 1 و 4.")

    # Generate text content using Hugging Face's Mistral model
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
                    # if level == 2:
                    #     return {"level": level, "exercise": text_content}


    except Exception as e:
            raise HTTPException(status_code=500, detail=f"حدث خطأ أثناء توليد النص: {e}")

    
    # Extract the question (everything before the first choice)
    question = text_content.split("أ)")[0].strip()

    # Extract the choices
    choices_part = text_content.split("أ)")[1].strip()
    choices = {
        "أ": choices_part.split("ب)")[0].strip(),
        "ب": choices_part.split("ب)")[1].split("ج)")[0].strip(),
        "ج": choices_part.split("ج)")[1].strip()
    }

    # Determine the correct answer (assuming the first choice is correct)
   # correct_answer = "أ" 


    return {
        "level": level,
        "question": question,
        "choices": choices,
      #  "correct_answer": correct_answer
    }
    