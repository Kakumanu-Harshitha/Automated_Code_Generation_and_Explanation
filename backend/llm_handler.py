# llm_handler.py
from groq import Groq
import re

class LLMCodeHandler:
    """Handles all interactions with the LLM for code generation, explanation, and optimization."""

    def __init__(self, api_key: str, model: str):
        self.client = Groq(api_key=api_key)
        self.model = model

    def _parse_response(self, text: str, headers: list) -> dict:
        """Parses the LLM response based on markdown headers (e.g., ## Code)."""
        response = {}
        for i, header in enumerate(headers):
            next_header = headers[i+1] if i + 1 < len(headers) else None
            pattern = rf"##\s*{header}\s*\n(.*?)(?=##\s*{next_header}|$)"
            match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
            
            if match:
                content = match.group(1).strip()
                code_match = re.search(r"```[a-zA-Z]*\n(.*?)\n```", content, re.DOTALL)
                if code_match:
                    response[header.lower()] = code_match.group(1).strip()
                else:
                    response[header.lower()] = content
            else:
                 response[header.lower()] = ""
        return response

    def generate_with_explanation(self, problem_description: str, language: str) -> tuple[str, str]:
        """Generates code and an explanation. Returns a tuple: (code, explanation)."""
        prompt = f"""
        You are an expert {language} programmer and a skilled technical writer.
        Solve the following problem in {language}.

        **Problem:**
        {problem_description}

        Your response must be structured in two parts with these exact markdown headers:
        1. `## Code`: This section must contain only the complete, compilable {language} code.
        2. `## Explanation`: This section must explain the code's logic and approach.
        """
        try:
            chat_completion = self.client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model=self.model,
                temperature=0.2,
            )
            response_text = chat_completion.choices[0].message.content
            parsed_data = self._parse_response(response_text, ["Code", "Explanation"])
            return parsed_data.get("code", "Error: Could not parse code."), \
                   parsed_data.get("explanation", "Error: Could not parse explanation.")
        except Exception as e:
            return f"An error occurred: {e}", ""

    def optimize_code(self, problem_description: str, original_code: str, language: str) -> tuple[str, str]:
        """Optimizes code and explains the changes. Returns a tuple: (optimized_code, optimization_explanation)."""
        prompt = f"""
        You are a world-class software engineer specializing in code optimization for {language}.
        Review the following code, which was written for the problem described below.

        **Problem:**
        {problem_description}

        **Original {language} Code:**
        ```
        {original_code}
        ```

        Your task is to rewrite the code to be more optimal in terms of performance (time complexity, space complexity) or readability, without sacrificing correctness.

        Your response must be structured in two parts with these exact markdown headers:
        1. `## Optimized Code`: This section must contain only the complete, optimized {language} code.
        2. `## Optimization Explanation`: This section must clearly explain what you changed and why those changes lead to a more optimal solution.
        """
        try:
            chat_completion = self.client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model=self.model,
            temperature=0.4,
            )
            response_text = chat_completion.choices[0].message.content
            parsed_data = self._parse_response(response_text, ["Optimized Code", "Optimization Explanation"])
        
            return parsed_data.get("optimized code", "Error: Could not parse optimized code."), \
               parsed_data.get("optimization explanation", "Error: Could not parse optimization explanation.")
               
        except Exception as e:
            return f"An error occurred during optimization: {e}", ""