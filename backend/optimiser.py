from backend.llm_handler import LLMCodeHandler

class CodeOptimizer:
    """Uses LLMCodeHandler to optimize code."""

    def __init__(self, llm_handler: LLMCodeHandler):
        self.llm = llm_handler

    def optimize(self, problem_description: str, code: str, language: str):
        optimized_code, explanation = self.llm.optimize_code(problem_description, code, language)
        return optimized_code, explanation
