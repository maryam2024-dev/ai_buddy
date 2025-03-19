from fastapi import APIRouter, HTTPException
from datetime import datetime
import os
import shutil
import requests
from gradio_client import Client

router = APIRouter()

# Directory to save images locally
IMAGE_SAVE_DIR = "cartoon_images"
os.makedirs(IMAGE_SAVE_DIR, exist_ok=True)

# Gradio Client Initialization
GRADIO_MODEL = "stabilityai/stable-diffusion-3-medium"

@router.post("/generate-gradio", status_code=201)
async def generate_image_with_gradio(prompt: str):
    """
    Generate an image using the Gradio client for Stability AI's model.
    """
    try:
        print("Connecting to Gradio client...")
        client = Client(GRADIO_MODEL)

        print(f"Generating image for prompt: {prompt}")
        result = client.predict(
            prompt=prompt,
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

        # Extract and validate the image path or URL
        image_url = result[0]  
        if not image_url:
            raise HTTPException(status_code=400, detail="Invalid image result received.")

        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        image_filename = f"gradio_{timestamp}.png"
        image_path = os.path.join(IMAGE_SAVE_DIR, image_filename)

      
        image_data = requests.get(image_url).content
        with open(image_path, "wb") as f:
            f.write(image_data)
        
        # else:
        #     raise HTTPException(status_code=400, detail="Generated image not found.")

        print(f"Image saved at: {image_path}")
        return {"image_path": image_path}

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to generate image: {e}")


