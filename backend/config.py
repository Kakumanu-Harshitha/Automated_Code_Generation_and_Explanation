import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
LLM_MODEL_NAME = "gemma2-9b-it" 
if not GROQ_API_KEY:
    raise ValueError("Groq API key not found. Please set it in .env file.")
