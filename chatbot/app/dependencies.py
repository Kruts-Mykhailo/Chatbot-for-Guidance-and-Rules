from fastapi import FastAPI

from app.core.embedding.embeddings_generator_factory import get_generator
from app.core.language_models.llm_factory import get_llm_instance
from app.core.retrieval.vector_search_factory import get_solution
from app.services.secrets.retriever_factory import get_retriever_instance

# Global variables for dependencies
vector_search = None
embedding_generator = None
model = None
secrets_retriever = None


async def init_dependencies(app: FastAPI, args):
    """
    Initialize dependencies with command-line arguments.
    """
    global vector_search, embedding_generator, model, secrets_retriever

    # Use the parsed arguments to initialize dependencies
    search_type = args.search_type
    generator_type = args.generator_type
    model_type = args.model_type
    secrets_type = args.secret_type

    # Initialize Vector Search
    vector_search = get_solution(search_type)
    vector_search.connect()

    # Initialize Embedding Generator
    embedding_generator = get_generator(generator_type)
    
    # Initialize secrets retriever
    secrets_retriever = get_retriever_instance(secrets_type)

    # Initialize Language Model
    model = get_llm_instance(model_type, secrets_retriever=secrets_retriever)
    
    
    # Store in app state for centralized access
    app.state.vector_search = vector_search
    app.state.embedding_generator = embedding_generator
    app.state.model = model
    app.state.secrets_retriever = secrets_retriever


async def shutdown_dependencies(app: FastAPI):
    """
    Shutdown dependencies and release resources.
    """
    global vector_search, embedding_generator, model, secrets_retriever

    if vector_search:
        vector_search.close()
        vector_search = None

    embedding_generator = None
    model = None
    secrets_retriever = None


def get_vector_search():
    """
    Dependency for vector search.
    """
    if not vector_search:
        raise RuntimeError("Vector search not initialized")
    return vector_search


def get_embedding_generator():
    """
    Dependency for embedding generator.
    """
    if not embedding_generator:
        raise RuntimeError("Embedding generator not initialized")
    return embedding_generator


def get_model():
    """
    Dependency for large langauge model.
    """
    if not model:
        raise RuntimeError("Model not initialized")
    return model


def get_secrets_retriever():
    """
    Dependency for secrets retriever.
    """
    if not secrets_retriever:
        raise RuntimeError("Secrets retriever not initialized")
    return secrets_retriever