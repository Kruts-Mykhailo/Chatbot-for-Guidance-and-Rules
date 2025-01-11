from uu import Error
from openai import OpenAI
from typing import Any, Iterable
from app.core.language_models.llm_abstract import BaseLLM
import os

class ChatGPTLLM(BaseLLM):
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.model = "gpt-4o-mini"
        
        if not self.api_key:
            return "Error: OPENAI_API_KEY environment variable is not set."
        
        self.client = OpenAI(api_key=self.api_key)

    def generate(self, prompt: str, **kwargs) -> str:
        query = kwargs.get("query", None)
        messages: Iterable[Any] = [{"role": "system", "content": prompt}]

        if query:
            messages.append({"role": "user", "content": query})

        try:
            # Call the OpenAI API
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=messages
            )
            response = completion.choices[0].message.content
            if not response:
                raise Error("Error no response text from chatGPT")
            return response
        except Exception as e:
            return f"Error: {e}"