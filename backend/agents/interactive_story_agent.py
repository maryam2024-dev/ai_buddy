from datetime import datetime
import shutil
from fastapi import FastAPI, HTTPException, APIRouter, Body
from pydantic import BaseModel
from typing import List, Optional, Dict
from openai import OpenAI
import os
from gradio_client import Client
from utils.load_helper import HUGGINGFACE_TOKEN
router = APIRouter()

# Directory to save images locally
IMAGE_SAVE_DIR = "interactive_images"
os.makedirs(IMAGE_SAVE_DIR, exist_ok=True)

# Gradio Client Initialization
# = "stabilityai/stable-diffusion-3-medium"
GRADIO_MODEL="agents-course/text-to-image"

# Initialize Hugging Face client
hf_client = OpenAI(
    base_url="https://router.huggingface.co/novita",
    api_key=HUGGINGFACE_TOKEN
)

class StorySegment(BaseModel):
    text: str
    choices: List[str] = []  # Two choices for each segment
    image_path: Optional[str] = None
    branches: Optional[Dict[str, "StorySegment"]] = None  # Nested branches for each choice

@router.post("/generate_story", status_code=201)
async def generate_story():
    """
    Generate an entire interactive story with all possible branches and choices.

    Returns:
        dict: A dictionary containing the entire story tree with segments and choices.
    """
    try:
        # Generate the entire story tree
        story_tree = await _generate_story_segment()

        return {
            "story_tree": story_tree
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to generate or parse AI response: {e}")

async def _generate_story_segment(depth: int = 0, max_depth: int = 2) -> Dict:
    """
    Recursively generate a story segment with two choices and their branches.

    Parameters:
        depth (int): Current depth of the story tree.
        max_depth (int): Maximum depth of the story tree.

    Returns:
        dict: A dictionary representing the story segment and its branches.
    """
    if depth >= max_depth:
        return None

    # Generate the story segment (shorter version)
    full_prompt = (
        "Write a very short, creative, and engaging story for children in 1-2 sentences. "
        "At the end, provide two distinct choices for what happens next."
    )

    response = hf_client.chat.completions.create(
        model="meta-llama/llama-3-70b-instruct",
        messages=[{"role": "user", "content": full_prompt}],
    )
    
    if hasattr(response, "choices") and response.choices:
        first_choice = response.choices[0]
        if hasattr(first_choice, "message") and hasattr(first_choice.message, "content"):
            text_content = first_choice.message.content.strip()
            print(f"text_content: {text_content}")
        else:
            raise HTTPException(status_code=400, detail="Unexpected response format from Hugging Face API.")
    else:
        raise HTTPException(status_code=400, detail="No response choices found from Hugging Face API.")
    
    # Generate an image prompt based on the story
    image_prompt = f"A colorful, dreamy children's illustration for a story about {text_content}. Whimsical and magical style with soft painterly textures, fantasy elements, and warm pastel colors."

    # Define panorama dimensions
    print("Connecting to Gradio client...")
        # client_gradio = Client(GRADIO_MODEL)
    client = Client("agents-course/text-to-image")

    print(f"Generating image for prompt: {image_prompt}")
        
        
    result = client.predict(
                param_0=image_prompt,
                api_name="/predict"
        )
    if isinstance(result, (list, tuple)) and len(result) > 0:
            gradio_image_path = result[0]  # First element is the file path
    else:
            gradio_image_path = result

            
    # Save the image locally
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    image_filename = f"gradio_{timestamp}.png"
    image_path = os.path.join(IMAGE_SAVE_DIR, image_filename)
    shutil.copy(gradio_image_path, image_path)
    print(f"Image copied to: {image_path}")

    # Construct the public URL for the image
    public_image_url = f"http://127.0.0.1:8000/{image_path}"
    print(f"Public image URL: {public_image_url}")

    # Create the current story segment
    current_segment = {
        "text": text_content,
        "choices": ["First Choice", "Second Choice"],  # Two choices for branching
        "image_url": public_image_url,
        "branches": {}  # Branches for the next segments
    }

    # Recursively generate branches for each choice
    for choice in current_segment["choices"]:
        branch = await _generate_story_segment(depth + 1, max_depth)
        if branch:
            current_segment["branches"][choice] = branch

    return current_segment