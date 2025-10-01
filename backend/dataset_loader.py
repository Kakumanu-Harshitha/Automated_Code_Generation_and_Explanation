from datasets import load_dataset

def load_code_contests():
    """Load DeepMind code_contests dataset."""
    dataset = load_dataset("deepmind/code_contests")
    return dataset["train"], dataset["valid"], dataset["test"]

def preprocess_sample(sample, language="Python"):
    """Convert sample into prompt-completion format."""
    problem_desc = sample["description"]
    solution_code = sample["solutions"][0]
    prompt = f"Write a {language} function for this problem:\n{problem_desc}\n"
    return {"prompt": prompt, "completion": solution_code}
