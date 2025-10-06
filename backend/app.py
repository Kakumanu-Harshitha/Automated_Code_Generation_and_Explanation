from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware

from backend import config
from backend.llm_handler import LLMCodeHandler
from backend.optimiser import CodeOptimizer
# The dataset loader is no longer imported because it uses too much memory.
# from backend.dataset_loader import load_code_contests 

# --- Initialize system ---
llm_handler = LLMCodeHandler(api_key=config.GROQ_API_KEY, model=config.LLM_MODEL_NAME)
optimizer = CodeOptimizer(llm_handler)

# This line, which causes the "Out of Memory" error, has been removed.
# train, valid, test = load_code_contests()

app = FastAPI(title="AI Code Assistant API")

# Allow CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

class CodeRequest(BaseModel):
    problem_description: str
    language: str

class OptimizeRequest(BaseModel):
    problem_description: str
    language: str
    code: str

@app.get("/")
def read_root():
    return {"message": "AI Code Assistant API is running!"}

@app.post("/generate_code")
def generate_code_with_analysis(request: CodeRequest):
    if not request.problem_description.strip():
        raise HTTPException(status_code=400, detail="Problem description cannot be empty.")
    
    analysis_result = llm_handler.generate_with_analysis(request.problem_description, request.language)
    return analysis_result

@app.post("/optimize_code")
def optimize_code_with_analysis(request: OptimizeRequest):
    if not request.code.strip():
        raise HTTPException(status_code=400, detail="Original code cannot be empty.")

    analysis_result = optimizer.optimize_and_analyze(request.problem_description, request.code, request.language)
    return analysis_result

