import json
import re
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from together import Together
from openai import OpenAI
from utils.load_helper import OPENAI_API_KEY_TOGETHER, HUGGINGFACE_TOKEN

router = APIRouter()

# Initialize clients
client_together = Together(api_key=OPENAI_API_KEY_TOGETHER)
client = OpenAI(
    base_url="https://router.huggingface.co/novita",
    api_key=HUGGINGFACE_TOKEN
)

# Define request model
class GenerateMathRequest(BaseModel):
    level: int = Field(..., description="The difficulty level of the math question. Choose 1, 2, 3, or 4.")

@router.post("/generate-math", status_code=201)
async def generate_math_questions(request: GenerateMathRequest):
    """
    Generate math questions for kids in Arabic with structured JSON output.
    """
    level = request.level

    prompts = {
    1: "Create a simple addition problem for children with ٣ answer choices. "
    " one the 3 answer is the correct ansewr which also return it"
       "The response must be JSON only, without any comments or explanations: "
       "{\"question\": \"...\", \"choices\": {\"أ\": \"...\", \"ب\": \"...\", \"ج\": \"...\"}, \"correct_answer\": \"...\"}",
    2: "Create a simple subtraction problem for children with ٣ answer choices. "
    " one the 3 answer is the correct ansewr which also return it"
       "The response must be JSON only, without any comments or explanations: "
       "{\"question\": \"...\", \"choices\": {\"أ\": \"...\", \"ب\": \"...\", \"ج\": \"...\"}, \"correct_answer\": \"...\"}",
    3: "Create a simple counting problem for children with ٣ answer choices. "
    " one the 3 answer is the correct ansewr which also return it"
       "The response must be JSON only, without any comments or explanations: "
       "{\"question\": \"...\", \"choices\": {\"أ\": \"...\", \"ب\": \"...\", \"ج\": \"...\"}, \"correct_answer\": \"...\"}",
    4: "Create a simple comparison problem for children with ٣ answer choices. "
    " one the 3 answer is the correct ansewr which also return it"
       "The response must be JSON only, without any comments or explanations: "
       "{\"question\": \"...\", \"choices\": {\"أ\": \"...\", \"ب\": \"...\", \"ج\": \"...\"}, \"correct_answer\": \"...\"}",
    # 5: "Create a problem for children asking how many balls (or any other object) are there in the image, with ٣ answer choices. "
    #    "One of the 3 answers is the correct answer, which is the number of balls, and the other two answers are incorrect. "
    #    "Also, generate a relevant image that visually represents this question."
    #    "The response must be JSON only, without any comments or explanations: "
    #    "{\"question\": \"How many balls are there?\", \"choices\": {\"أ\": \"...\", \"ب\": \"...\", \"ج\": \"...\"}, \"correct_answer\": \"...\", \"image_url\": \"...\"}"
    }

    if level not in prompts:
        raise HTTPException(status_code=400, detail="المستوى غير صحيح. اختر مستوى بين 1 و 4.")

    text_prompt = prompts[level]

    # Call AI model
    try:
        response = client.chat.completions.create(
            model="meta-llama/llama-3-70b-instruct",
            messages=[{"role": "user", "content": text_prompt}]
        )

        if hasattr(response, "choices") and response.choices:
            first_choice = response.choices[0]

            if hasattr(first_choice, "message") and hasattr(first_choice.message, "content"):
                json_response = first_choice.message.content.strip()
            else:
                raise ValueError("Response format incorrect")
        else:
            raise ValueError("No choices returned from model")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"حدث خطأ أثناء توليد النص: {e}")

    try:
        # Use regex to extract only the JSON part
        match = re.search(r"(\{.*\})", json_response, re.DOTALL)

        if match:
            json_response = match.group(1)  # Extract only JSON content
            try:
                structured_data = json.loads(json_response)  # Convert to dictionary
                print(json.dumps(structured_data, ensure_ascii=False))  # Print clean JSON
            except json.JSONDecodeError as e:
                print(f"Invalid JSON: {e}")
        else:
            print("No valid JSON found.")
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="تعذر تحليل البيانات المُولدة بتنسيق JSON.")
    
     # For level 5: Generate an image and include the image URL
    if level == 5:
        # Placeholder for image generation, replace with actual image generation logic or URL
        image_url = "https://example.com/image_of_balls.jpg"  # You can replace this URL with an actual image URL from an image generation API or service.

        # Add image URL to the structured data
        structured_data["image_url"] = image_url

    # Add logic to include the correct answer in the returned response
    correct_answer = structured_data.get("correct_answer", None)
    if correct_answer:
        structured_data["correct_answer"] = correct_answer

    return {
        "level": level,
        **structured_data
    }
