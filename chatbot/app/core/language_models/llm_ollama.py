from app.core.language_models.llm_abstract import BaseLLM
import ollama

OLLAMA_MODEL="llama2"

class OllamaLLM(BaseLLM):
    
    def __init__(self):
        self.model = OLLAMA_MODEL

    def generate(self, prompt: str, **kwargs) -> str:
        query = kwargs.get('query', None)
        messages = [{"role": "user", "content": prompt}]

        if query:
            messages.append({"role": "user", "content": query})

        response = ollama.chat(model=OLLAMA_MODEL, messages=messages)

        if 'message' in response and 'content' in response['message']:
            return response['message']['content']
        else:
            return "Sorry, I couldn't retrieve a valid response from the model."
        