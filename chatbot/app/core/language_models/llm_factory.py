from app.core.language_models.llm_abstract import BaseLLM
from app.core.language_models.llm_ollama import OllamaLLM
from app.core.language_models.llm_chatgpt import ChatGPTLLM


def get_llm_instance(llm_type: str, **kwargs) -> BaseLLM:
    """
    Factory function to create an instance of the requested LLM implementation.

    :param llm_type: The type of LLM to instantiate (e.g., "openai", "ollama").

    :return: An instance of a class that implements BaseLLM.
    """
    if llm_type == "ollama":
        return OllamaLLM()
    if llm_type == "openai":
        secrets_retriever = kwargs.get("secrets_retriever", None)
        return ChatGPTLLM(secrets_retriever)
    else:
        raise ValueError(f"Unsupported LLM type: {llm_type}")


def construct_prompt(category: str, retrieved_text: str) -> str:
    return f"""
    You are a friendly and helpful assistant. Your primary role is to provide concise, accurate, and clear answers strictly based on the retrieved text below. 

    Rules for your response:
    - Always answer the user's question directly using only the information provided in the retrieved text.
    - Do not ask the user for clarification or respond with general comments such as "What do you want to know about X?"
    - Avoid unnecessary preambles or restatements of the user's question.
    Below is the {category} retrieved from the knowledge base. You do not have prior knowledge and must use only this information:

    {retrieved_text}

    Answer the user's question strictly using information above that has been retrieved.
    """
