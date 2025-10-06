from groq import Groq
import re

class LLMCodeHandler:
    """Handles all interactions with the LLM for code generation, explanation, and optimization."""

    def __init__(self, api_key: str, model: str):
        self.client = Groq(api_key=api_key)
        self.model = model

    def _parse_response(self, text: str, headers: list) -> dict:
        """Parses the LLM response based on markdown headers and normalizes keys."""
        response = {}
        for i, header in enumerate(headers):
            # Convert header to a snake_case key, e.g., "Time Complexity" -> "time_complexity"
            key = header.lower().replace(" ", "_")
            
            next_header = headers[i+1] if i + 1 < len(headers) else None
            # Regex to find content between the current header and the next one (or end of string)
            pattern = rf"##\s*{header}\s*\n(.*?)(?=##\s*{next_header}|$)"
            match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
            
            if match:
                content = match.group(1).strip()
                # Extract code only from within ```...``` blocks if they exist
                code_match = re.search(r"```[a-zA-Z]*\n(.*?)\n```", content, re.DOTALL)
                if code_match:
                    response[key] = code_match.group(1).strip()
                else:
                    response[key] = content
            else:
                response[key] = ""
        return response

    def generate_with_analysis(self, problem_description: str, language: str) -> dict:
        """Generates code and provides a full analysis including complexity."""
        prompt = f"""
        You are an expert {language} programmer and a skilled technical writer specializing in algorithm analysis.
        Solve the following problem in {language}.

        **Problem:**
        {problem_description}

        Your response must be structured in four parts with these exact markdown headers:
        1. `## Code`: This section must contain only the complete, compilable {language} code.
        2. `## Explanation`: This section must explain the code's logic and approach.
        3. `## Time Complexity`: This section must provide and briefly justify the Big O notation for the time complexity (e.g., O(n log n)).
        4. `## Space Complexity`: This section must provide and briefly justify the Big O notation for the space complexity (e.g., O(n)).
        """
        try:
            chat_completion = self.client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model=self.model,
                temperature=0.2,
            )
            response_text = chat_completion.choices[0].message.content
            headers = ["Code", "Explanation", "Time Complexity", "Space Complexity"]
            return self._parse_response(response_text, headers)
        except Exception as e:
            return {"error": f"An error occurred: {e}"}

    def optimize_and_analyze(self, problem_description: str, original_code: str, language: str) -> dict:
        """Optimizes code and provides a full analysis of the changes."""
        prompt = f"""
        You are a world-class software engineer specializing in code optimization and algorithm analysis for {language}.
        Review the following code, which was written for the problem described below.

        **Problem:**
        {problem_description}

        **Original {language} Code:**
        ```
        {original_code}
        ```

        Your task is to analyze the original code, then rewrite it to be more optimal.

        Your response must be structured in six parts with these exact markdown headers:
        1. `## Original Time Complexity`: Analyze and provide the Big O notation for the original code's time complexity.
        2. `## Original Space Complexity`: Analyze and provide the Big O notation for the original code's space complexity.
        3. `## Optimized Code`: This section must contain only the complete, optimized {language} code.
        4. `## Optimized Time Complexity`: Provide the Big O notation for your optimized code's time complexity.
        5. `## Optimized Space Complexity`: Provide the Big O notation for your optimized code's space complexity.
        6. `## Optimization Explanation`: This section must clearly explain what you changed and why those changes lead to a more optimal solution, referencing the complexity improvements.
        """
        try:
            chat_completion = self.client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model=self.model,
                temperature=0.4,
            )
            response_text = chat_completion.choices[0].message.content
            headers = [
                "Original Time Complexity", "Original Space Complexity",
                "Optimized Code", "Optimized Time Complexity",
                "Optimized Space Complexity", "Optimization Explanation"
            ]
            parsed_data = self._parse_response(response_text, headers)

            # Map parsed keys to the keys expected by the frontend
            return {
                "original_complexity": parsed_data.get("original_time_complexity", "N/A"),
                "original_space_complexity": parsed_data.get("original_space_complexity", "N/A"),
                "optimized_code": parsed_data.get("optimized_code", "Error parsing code."),
                "optimized_complexity": parsed_data.get("optimized_time_complexity", "N/A"),
                "optimized_space_complexity": parsed_data.get("optimized_space_complexity", "N/A"),
                "optimization_explanation": parsed_data.get("optimization_explanation", "Error parsing explanation."),
            }
        except Exception as e:
            return {"error": f"An error occurred during optimization: {e}"}
