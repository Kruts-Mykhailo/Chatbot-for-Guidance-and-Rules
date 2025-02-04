import argparse
import asyncio
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

import uvicorn
from fastapi import FastAPI

from app.dependencies import init_dependencies, shutdown_dependencies
from app.external_services.rabbitmq_consumer import (
    add_queue_handler,
    process_game_added_event,
    start_all_queue_listeners,
)
from app.routers.chat import chat_router

load_dotenv()

GAMEPLATFORM_URL = os.getenv("GAMEPLATFORM_URL")

if not GAMEPLATFORM_URL:
    raise ValueError("GAMEPLATFORM_URL environment variable is not set or empty.")

def parse_args():
    parser = argparse.ArgumentParser(description="RAG Chatbot Microservice")
    parser.add_argument(
        "--search_type",
        type=str,
        required=True,
        help="Type of vector search (e.g., pgvector)",
    )
    parser.add_argument(
        "--generator_type",
        type=str,
        required=True,
        help="Type of embedding generator (e.g., sentence_transformer)",
    )
    parser.add_argument(
        "--model_type",
        type=str,
        required=True,
        help="Type of model for RAG (e.g., ollama)",
    )
    parser.add_argument(
        "--secret_type",
        type=str,
        required=True,
        help="Type of secrets retriever (e.g., local, gcloud)",
    )
    return parser.parse_args()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for application startup and shutdown.
    """
    args = parse_args()
    await init_dependencies(app, args)

    vector_search = app.state.vector_search
    embedding_generator = app.state.embedding_generator
    secrets_retriever = app.state.secrets_retriever
    add_queue_handler(
        "new_rules_queue",
        lambda data: process_game_added_event(data, vector_search, embedding_generator),
    )
    rabbitmq_task = asyncio.create_task(start_all_queue_listeners())

    yield  # Application runs during this time

    # Shutdown tasks
    rabbitmq_task.cancel()
    await shutdown_dependencies(app)  # Clean up resources


# Initialize FastAPI app with lifespan
app = FastAPI(lifespan=lifespan, strict_slashes=False)

# Add CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[GAMEPLATFORM_URL],  
    allow_credentials=True,
    allow_methods=["POST"], 
    allow_headers=["*"],  
)

# Include routers
app.include_router(chat_router, prefix="/chat", tags=["Chat"])

# If running the app directly
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
