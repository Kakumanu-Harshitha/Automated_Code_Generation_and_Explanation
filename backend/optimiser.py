from .llm_handler import LLMCodeHandler

class CodeOptimizer:
    """Uses LLMCodeHandler to optimize code and provide analysis."""

    def __init__(self, llm_handler: LLMCodeHandler):
        self.llm = llm_handler

    def optimize_and_analyze(self, problem_description: str, code: str, language: str) -> dict:
        """
        Calls the handler to optimize and analyze code, returning the full analysis.
        This method acts as a pass-through to the llm_handler's more complex logic.
        """
        return self.llm.optimize_and_analyze(problem_description, code, language)
