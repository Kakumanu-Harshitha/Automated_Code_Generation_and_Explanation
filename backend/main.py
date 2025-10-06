# This file is used to initialize all components and can be used for testing.
# It is not required to run the web application but is good practice.

from backend import config
from backend.llm_handler import LLMCodeHandler
from backend.optimiser import CodeOptimizer
from backend.dataset_loader import load_code_contests

def initialize_system():
    """Initialize all core components of the backend."""
    print("Initializing system...")
    llm_handler = LLMCodeHandler(api_key=config.GROQ_API_KEY, model=config.LLM_MODEL_NAME)
    optimizer = CodeOptimizer(llm_handler)
    print("Loading dataset...")
    train, valid, test = load_code_contests()
    print("Dataset loaded.")
    return llm_handler, optimizer, train, valid, test

if __name__ == "__main__":
    try:
        llm_handler, optimizer, train, valid, test = initialize_system()
        print("✅ System initialized successfully.")
        print(f"Train samples: {len(train)}, Valid samples: {len(valid)}, Test samples: {len(test)}")

        # --- Quick Test ---
        print("\n--- Running a quick generation test ---")
        problem = "Write a Python function to compute the factorial of a number using recursion."
        
        # Using the new analysis method
        result = llm_handler.generate_with_analysis(problem, "Python")

        if "error" not in result:
            print("\nGenerated Code:\n", result.get("code"))
            print("\nTime Complexity:", result.get("time_complexity"))
            print("\nSpace Complexity:", result.get("space_complexity"))
            print("\nExplanation:\n", result.get("explanation"))
        else:
            print("\nError during test:", result.get("error"))

    except Exception as e:
        print(f"An error occurred during initialization: {e}")
