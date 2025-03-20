import base64
from datetime import datetime
import json
import os
from pathlib import Path
import random
import re
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
from huggingface_hub import InferenceClient



router = APIRouter()


# Set up headers with the API token
headers = {
    "Authorization": f"Bearer {HUGGINGFACE_TOKEN}",
    "Content-Type": "application/json"
}


client_inference = InferenceClient(
    provider="replicate",
    api_key=HUGGINGFACE_TOKEN,
)





# Function to encode an image file to base64
def encode_image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

# Function to get a description of the image using Hugging Face model
def get_image_description(image_path):
    # Encode the image to base64
    base64_image = encode_image_to_base64(image_path)

    # Prepare the payload for the Hugging Face API
    payload = {
        "inputs": base64_image,
        "parameters": {
            "max_length": 50,  # Limit the output length
            "language": "ar",  # Request Arabic language output
        },
    }

    # Send the request to the Hugging Face API
    response = requests.post(
        "https://api-inference.huggingface.co/models/black-forest-labs/FLUX.1-dev",
        headers=headers,
        json=payload,
    )

    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Error while generating image description.")

    # Parse the response
    description = response.json().get("generated_text", "").strip()
    return description

# Function to extract a single Arabic word from the description
def extract_arabic_word(description):
    # Use regex to extract the first Arabic word
    match = re.search(r"([\u0600-\u06FF]+)", description)
    if match:
        return match.group(1).strip()
    raise HTTPException(status_code=400, detail="Failed to extract an Arabic word from the description.")


# Assuming Together client is already initialized
# client_together = Together(api_key=OPENAI_API_KEY_TOGETHER)
client = OpenAI(
	base_url="https://router.huggingface.co/novita",
	api_key=HUGGINGFACE_TOKEN
)

# Local directory for storing images
IMAGE_DIR = Path("static/arabic_alphabetic_learning_images")
IMAGE_DIR.mkdir(exist_ok=True)


# Gradio Client Initialization
GRADIO_MODEL = "stabilityai/stable-diffusion-3-medium"

def get_random_image():
    """Select a random image from the directory."""
    if not IMAGE_DIR.exists() or not any(IMAGE_DIR.iterdir()):
        raise HTTPException(status_code=404, detail="No images found in the directory.")
    return random.choice(list(IMAGE_DIR.iterdir()))






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
        
       text_prompt = (
    "Return a list of three dictionaries, each representing an Arabic word. "
    "Each dictionary should include: "
    "- 'correct': a boolean (True for the correct word, False for the others), "
    "- 'arabic': the Arabic word, "
    "- 'english': the English translation of the word. "
    "Ensure exactly one word has 'correct': True, while the others have 'correct': False. "
    "Ensure the words are simple and suitable for kids. Do not add 'ال' unless it's part of the word. "
"A **common object or living being** that is frequently seen in everyday life, such as animals, plants, natural elements (e.g., sun, sea, moon), or familiar objects."    "all three word should be arabic words ."
    "Do not include any text, comments, explanations, or code blocks like ```python```. "
    "Do not return 'Sure! Here is the requested dictionary' or any explanatory text—only return the list of dictionaries. "
    "Example output:\n"
    "[\n"
    '    {"correct": true, "arabic": "شمس", "english": "sun"},\n'
    '    {"correct": false, "arabic": "قمر", "english": "moon"},\n'
    '    {"correct": false, "arabic": "نجم", "english": "star"}\n'
    "]"
)

# nd provide an image hint for the word.
    elif level == 2:
        text_prompt = (
            "Create a list of 4 Arabic words and a list of 4 Arabic letters. Ensure kids can match each word to its corresponding letter. "
            "Return the result as a JSON object with the following structure:\n"
            "{\n"
            '    "words": ["word1", "word2", "word3", "word4"],\n'
            '    "letters": ["letter1", "letter2", "letter3", "letter4"]\n'
            "}\n"
            "Ensure the words are simple and suitable for kids. Do not add 'ال' unless it's part of the word. "
            "Do not include any explanations, comments, or additional text—only return the JSON object."
            "Do not use any other language except arabic letters and words."
        )

    elif level == 3:
        text_prompt = (
    "Return a list of three dictionaries, each representing an Arabic verb that describes an action (e.g., playing, eating, swimming). "
    "Each dictionary should include: "
    "- 'correct': a boolean (True for the correct word, False for the others), "
    "- 'arabic': the Arabic verb, "
    "- 'english': the English translation of the verb. "
    "Ensure exactly one verb has 'correct': True, while the others have 'correct': False. "
    "Ensure the verbs are simple, commonly used, and suitable for kids. "
    "Do not add 'ال' unless it's part of the word. "
    "Do not include any text, comments, explanations, or code blocks like ```python```. "
    "Do not return 'Sure! Here is the requested dictionary' or any explanatory text—only return the list of dictionaries. "
    "Example output:\n"
    "[\n"
    '    {"correct": true, "arabic": "يلعب", "english": "playing"},\n'
    '    {"correct": false, "arabic": "يجري", "english": "running"},\n'
    '    {"correct": false, "arabic": "يرسم", "english": "drawing"}\n'
    "]"
)

        # text_prompt = (
        #    " Give me a simple and suitable for kids English word and its correct Arabic translation. "

        #     "Then, remove one letter from the Arabic word and replace it with an underscore (_) to create a word with a missing letter. "
        #     "Provide three Arabic letter options:"
        #     "- One of them Must be the removed letter from the word_with_missing_letter (the correct answer)."
        #     "- The other two should not exist in this Arabic word."

        #     "Ensure the result follows this JSON structure exactly:"

        #     "{\n"
        #     '   "word_with_missing_letter": "<Arabic word with missing letter>",\n'
        #     '   "options": ["<incorrect option 1>", "<correct option>", "<incorrect option 2>"],\n'
        #     '  "correct_option": "<correct option>",\n'
        #     '  "full_word_arabic": "<original Arabic word>",\n'
        #     '  "full_word_english": "<English word>"\n'
        #     "}\n"

        #     "Rules:"
        #     "- Ensure words are simple and suitable for kids."
        #     "- Do not add 'ال' unless it is part of the word."
        #     "- Do not include explanations or additional text—only return the JSON object."

        # )
        

    else:
        raise HTTPException(status_code=400, detail="Invalid level. Choose a level between 1 and 3.")

    # Generate text content
    try:
        print("Generating text content...")
#         client = Client("Rijgersberg/Qwen2.5-7B-Instruct")
#         response = client.predict(
#                 prompt=text_prompt,
#                 api_name="/chat"
# )
        response = client.chat.completions.create(
            model="meta-llama/llama-3-70b-instruct",
            messages=[{"role": "user", "content": text_prompt}],
        )

        # Extract the generated text content
        if hasattr(response, "choices") and response.choices:
            first_choice = response.choices[0]

            if hasattr(first_choice, "message") and hasattr(first_choice.message, "content"):
                text_content = first_choice.message.content.strip()
                # text_content=response.choices[0].message.content
                print(f"text_content: {text_content}")
                response=text_content
            else:
                raise HTTPException(status_code=400, detail="Unexpected response format from Hugging Face API.")
        else:
            raise HTTPException(status_code=400, detail="No response choices found from Hugging Face API.")
        if level == 1:
            print(response)
            print(type(response))
            if isinstance(response,str):
                print("response is str")
                response= str(response)
                print(type(response))
                try:
                    response = json.loads(response)
                except json.JSONDecodeError as e:
                    raise HTTPException(status_code=500, detail=f"JSON Decode Error: {e}")
                print(f" convert str to json:{response}")
                print(type(response))
            # response=text_content
                                
                               
                
            # Find the correct word and extract its English translation
            try:
                correct_english_word = next(value["english"] for value in response if value["correct"])
                correct_answer = next(value["arabic"] for value in response if value["correct"])
                print(f"Correct English Word: {correct_english_word}")
                print(f"Correct Arabic Answer: {correct_answer}")
            except StopIteration:
                raise HTTPException(status_code=500, detail="No correct word found in response.")
            image_prompt =  (f"A high-quality, realistic image of a {correct_english_word}."
                             "The image should be photorealistic, without any added text, letters, or symbols in any language. "
                             "Ensure the subject is a real-world object, animal. "
   "The image should feel natural and not artificially edited or computer-generated."
"No extra symbols, characters, or additional words in any language. " 

                             
                             )
            question="أي من هذه الكلمات تطابق الصورة؟"

        elif level == 2 :
            print(response)
            print(type(response))
            if isinstance(response,str):
                print("response is str")
                response= str(response)
                print(type(response))
                try:
                    response = json.loads(response)
                except json.JSONDecodeError as e:
                    raise HTTPException(status_code=500, detail=f"JSON Decode Error: {e}")
                print(f" convert str to json:{response}")
                print(type(response))
            question="طابق الكلمات مع الحروف الصحيحة."

            

            return {
        "level": level,
        "exercise": response,
        "image_url": None,
        "question":question
    }

        elif level==3:
            print(response)
            print(type(response))
            if isinstance(response,str):
                print("response is str")
                response= str(response)
                print(type(response))
                try:
                    response = json.loads(response)
                except json.JSONDecodeError as e:
                    raise HTTPException(status_code=500, detail=f"JSON Decode Error: {e}")
                print(f" convert str to json:{response}")
                print(type(response))
            
            
            # Find the correct word and extract its English translation
            try:
                correct_english_word = next(value["english"] for value in response if value["correct"])
                correct_answer = next(value["arabic"] for value in response if value["correct"])
                print(f"Correct English Word: {correct_english_word}")
                print(f"Correct Arabic Answer: {correct_answer}")
            except StopIteration:
                raise HTTPException(status_code=500, detail="No correct word found in response.")
            image_prompt = (
     f"A high-quality, **realistic** image of a human, such as a boy or girl,women,man, actively performing the action: {correct_english_word}. "
    "The image must **clearly depict** the action in a natural and lifelike manner. "
    "The action should be **easily recognizable** and not abstract, symbolic, or artificially exaggerated. "
    "Do **not** add any text, words, letters, or symbols in any language. "
    # "The image must feel **authentic, unedited, and true to life**, avoiding any digitally manipulated or AI-artifacts. "
    "Avoid cartoonish, fantasy, or surreal elements—focus on photorealism. "
    "The composition should be **well-lit, naturally colored, and visually appealing**."
  
)
            question="أي من هذه الأفعال يناسب الصورة؟"


            


            



    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error while generating text: {e}")

    # Generate image using Gradio client
    try:
        
        # output is a PIL.Image object
        # 
        print("Connecting to Gradio client...")
        client_gradio = Client(GRADIO_MODEL)
        # client = Client("agents-course/text-to-image")

        print(f"Generating image for prompt: {image_prompt}")
        
        
        # result = client.predict(
        #         param_0=image_prompt,
        #         api_name="/predict"
        # )
        # # print(result)

        print(f"Generating image for prompt: {image_prompt}")
        result = client_gradio.predict(
            prompt=image_prompt,
            negative_prompt="",
            seed=0,
            randomize_seed=True,
            width=512,
            height=512,
            guidance_scale=7.5,
            num_inference_steps=25,
            api_name="/infer"
        )

        print(f"Result from Gradio Client: {result}")  # Debugging line

        # Extract the file path from the result
        if isinstance(result, (list, tuple)) and len(result) > 0:
            gradio_image_path = result[0]  # First element is the file path
        else:
            gradio_image_path = result
            # raise HTTPException(status_code=400, detail="Invalid image result received.")

        # Save the image locally
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        image_filename = f"arabic_level_{level}_{timestamp}.png"
        image_path = IMAGE_DIR / image_filename

        shutil.copy(gradio_image_path, image_path)
        print(f"Image saved at: {image_path}")

        # Construct the public URL for the image
        public_image_url = f"http://127.0.0.1:8000/{image_path}"
        print(f"Public image URL: {public_image_url}")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error while generating image: {e}")

    return {
        "level": level,
        "exercise": response,
        "correct_word":correct_answer,
        "image_url": public_image_url,
          "question":question
    }
    
    

