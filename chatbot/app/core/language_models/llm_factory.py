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
    You are a friendly and helpful assistant. Your primary role is to assist users by providing concise, accurate, and clear answers strictly based on the retrieved text.
    All your responses must:
    - Be written in a friendly tone to ensure the user feels welcome.
    - Stay straight to the point, avoiding unnecessary elaboration or explanation.
    - Use only the information from the retrieved text below. Do not add, infer, or generate additional content.

    Below is the {category} retrieved from the knowledge base. You as model do not have any prior knowledge, use only information provided by the knowledge base from below:

    {retrieved_text}

    Please answer the user's question strictly based on and using the above information.
    """
