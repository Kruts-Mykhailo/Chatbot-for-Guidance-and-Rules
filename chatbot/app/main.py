import argparse
import asyncio
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from app.dependencies import init_dependencies, shutdown_dependencies
from app.external_services.rabbitmq_consumer import (
    add_queue_handler,
    process_game_added_event,
    start_all_queue_listeners,
)
from app.routers.chat import chat_router


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
    return parser.parse_args()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for application startup and shutdown.
    """
    args = parse_args()
    await init_dependencies(app, args)

    vector_search = app.state.vector_search
    add_queue_handler(
        "new_game_queue", lambda data: process_game_added_event(data, vector_search)
    )
    rabbitmq_task = asyncio.create_task(start_all_queue_listeners())

    yield  # Application runs during this time

    # Shutdown tasks
    rabbitmq_task.cancel()
    await shutdown_dependencies(app)  # Clean up resources


# Initialize FastAPI app with lifespan
app = FastAPI(lifespan=lifespan, strict_slashes=False)

# Include routers
app.include_router(chat_router, prefix="/chat", tags=["Chat"])

# If running the app directly
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
