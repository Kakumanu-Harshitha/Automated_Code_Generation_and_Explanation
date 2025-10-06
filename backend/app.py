from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware

# These imports are assumed to be correct for your project structure
from backend import config
from backend.llm_handler import LLMCodeHandler
from backend.optimiser import CodeOptimizer
from backend.dataset_loader import load_code_contests

# --- System Initialization ---
# This setup is assumed to be working correctly.
llm_handler = LLMCodeHandler(api_key=config.GROQ_API_KEY, model=config.LLM_MODEL_NAME)
optimizer = CodeOptimizer(llm_handler)
train, valid, test = load_code_contests()

app = FastAPI(title="AI Code Assistant API")

# --- Middleware ---
# Allow CORS for frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# --- Pydantic Models (Data Schemas) ---
class CodeRequest(BaseModel):
    problem_description: str
    language: str

class OptimizeRequest(BaseModel):
    problem_description: str
    language: str
    code: str

# --- API Endpoints ---
@app.get("/")
def read_root():
    return {"message": "AI Code Assistant API is running!"}

@app.post("/generate_code")
def generate_code_with_analysis_endpoint(request: CodeRequest):
    if not request.problem_description.strip():
        raise HTTPException(status_code=400, detail="Problem description cannot be empty.")
    
    result = llm_handler.generate_with_analysis(request.problem_description, request.language)
    return result

@app.post("/optimize_code")
def optimize_code_with_complexity_endpoint(request: OptimizeRequest):
    if not request.code.strip():
        raise HTTPException(status_code=400, detail="Original code cannot be empty.")
    
    result = optimizer.optimize_and_analyze(request.problem_description, request.code, request.language)
    return result

@app.get("/dataset_info")
def dataset_info():
    return {
        "train_samples": len(train),
        "valid_samples": len(valid),
        "test_samples": len(test)
    }

# --- Main execution block (for direct script running) ---
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=10000)

