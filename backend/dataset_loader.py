from datasets import load_dataset

def load_code_contests():
    """Load the DeepMind code_contests dataset from Hugging Face."""
    try:
        dataset = load_dataset("deepmind/code_contests")
        return dataset["train"], dataset["test"]
    except Exception as e:
        print(f"Failed to load dataset: {e}")
        # Return empty structures to prevent crashing the app on startup
        return [], []

def preprocess_sample(sample, language="Python"):
    """
    Utility function to convert a dataset sample into a 
    prompt-completion format for fine-tuning.
    """
    problem_desc = sample["description"]
    # Assuming at least one solution exists
    solution_code = sample["solutions"][0] if sample["solutions"] else ""
    prompt = f"Write a {language} function for this problem:\n{problem_desc}\n"
    return {"prompt": prompt, "completion": solution_code}
