
from app.services.secrets.retriever_abstract import BaseRetriever
from app.services.secrets.retriever_local import LocalSecretRetriever


def get_retriever_instance(impl: str) -> BaseRetriever:
    """
    Factory function to create an instance of the requested secrets retriever implementation.

    :param impl: The type of secrets retriever to instantiate (e.g., "local", "gcloud").

    :return: An instance of a class that implements BaseLLM.
    """
    if impl == "local":
        return LocalSecretRetriever()
    
    else:
        raise ValueError(f"Unsupported secrets retriever type: {impl}")

