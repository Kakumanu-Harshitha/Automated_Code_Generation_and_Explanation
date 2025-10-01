import config
from backend.llm_handler import LLMCodeHandler
from backend.optimiser import CodeOptimizer
from backend.dataset_loader import load_code_contests

def initialize_system():
    """Initialize all core components."""
    llm_handler = LLMCodeHandler(api_key=config.GROQ_API_KEY, model=config.LLM_MODEL_NAME)
    optimizer = CodeOptimizer(llm_handler)
    train, valid, test = load_code_contests()
    return llm_handler, optimizer, train, valid, test

if __name__ == "__main__":
    llm_handler, optimizer, train, valid, test = initialize_system()
    print("✅ System initialized successfully.")
    print(f"Train samples: {len(train)}, Valid samples: {len(valid)}, Test samples: {len(test)}")

    # Quick test (optional)
    problem = "Write a function to compute factorial of a number."
    code, explanation = llm_handler.generate_with_explanation(problem, "Python")
    print("\nGenerated Code:\n", code)
    print("\nExplanation:\n", explanation)
