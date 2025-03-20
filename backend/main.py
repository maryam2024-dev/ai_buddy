import secrets
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from agents.normal_story_agent import router as normal_story_agent_router
from agents.interactive_story_agent import router as interactive_story_agent_router
# from agents.evaluaetion_agent import router as evaluaetion_agent_router
from agents.alpabet_arab_agent import router as alpabet_arab_agent_router
from agents.alpabet_eng_agent import router as alpabet_eng_agent_router
from agents.alpabet_eng_agent import router as alpabet_eng_agent_router
from agents.generate_image import router as generate_image_agent_router
from agents.mathematic_agent import router as mathematic_agent_router
from routes.user_route import router as user_router








# Initialize FastAPI
app = FastAPI(
    title="AI Buddy",
    description="API for managing AI Buddy API",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)




# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Setup Jinja2 templates
templates = Jinja2Templates(directory="templates")

# Include routers
app.include_router(normal_story_agent_router, prefix="/api/normal-story", tags=["Bedtime Stories"])
app.include_router(interactive_story_agent_router, prefix="/api/interactive-story", tags=["Interactive Stories"])
app.include_router(alpabet_arab_agent_router, prefix="/api/alpabet-arab", tags=["Alpabet Arabs"])
app.include_router(alpabet_eng_agent_router, prefix="/api/alpabet-eng", tags=["Alpabet English"])
app.include_router(alpabet_eng_agent_router, prefix="/api/alpabet-eng", tags=["Alpabet English"])
app.include_router(generate_image_agent_router, prefix="/api/generate-image", tags=["Generate Image"])
app.include_router(mathematic_agent_router, prefix="/api/mathematic", tags=["Mathematic"])
app.include_router(user_router, prefix="/api/user", tags=["auth"])
# app.include_router(evaluaetion_agent_router, prefix="/api/evaluaetion", tags=["Evaluaetion"])








if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
