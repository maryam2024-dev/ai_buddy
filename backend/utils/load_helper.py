from dotenv import load_dotenv
import os


load_dotenv()


# # ai models keys 
OPENAI_API_KEY_TOGETHER=os.getenv("OPENAI_API_KEY_TOGETHER")
HUGGINGFACE_TOKEN=os.getenv("HUGGINGFACE_TOKEN")
OPENAI_API_KEY=os.getenv("OPENAI_API_KEY")
# database connection
DATABASE_NAME=os.getenv("DATABASE_NAME")
DATABASE_HOST=os.getenv("DATABASE_HOST")

SECRET_KEY=os.getenv("SECRET_KEY")



