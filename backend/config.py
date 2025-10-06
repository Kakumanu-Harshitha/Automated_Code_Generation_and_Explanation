import os
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# --- Environment Variables ---
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
LLM_MODEL_NAME = "gemma2-9b-it"  # Or any other model you prefer

# --- Validation ---
if not GROQ_API_KEY:
    raise ValueError("Groq API key not found. Please set GROQ_API_KEY in your .env file.")
