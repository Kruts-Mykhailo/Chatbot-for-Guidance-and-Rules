import asyncio
import json
from logging.config import dictConfig
import os
import logging

from aio_pika import connect
from dotenv import load_dotenv

from app.configurations.guidance_loader import get_rules_category
from app.core.embedding.embeddings_generator_abstract import EmbeddingGenerator
from app.core.retrieval.vector_search_abstract import VectorSearch
from app.external_services.event_model import GameAddedEvent
from app.services.game_query_generator import generate_example_queries
from app.configurations.logging_config import LOGGING_CONFIG

dictConfig(LOGGING_CONFIG)


# Load environment variables
load_dotenv()

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")
RABBITMQ_PORT = int(os.getenv("RABBITMQ_PORT", 5672))
RABBITMQ_USER = os.getenv("RABBITMQ_USER", "guest")
RABBITMQ_PASSWORD = os.getenv("RABBITMQ_PASSWORD", "guest")

# Dictionary to store queue handlers
queue_handlers = {}


async def register_queue_listener(queue_name, handler):
    """
    Register a listener for a specific RabbitMQ queue.
    :param queue_name: Name of the RabbitMQ queue to listen to.
    :param handler: Async function to process messages from the queue.
    """
    connection = await connect(
        f"amqp://{RABBITMQ_USER}:{RABBITMQ_PASSWORD}@{RABBITMQ_HOST}:{RABBITMQ_PORT}/"
    )
    async with connection:
        channel = await connection.channel()
        queue = await channel.declare_queue(queue_name, durable=True)

        async with queue.iterator() as queue_iter:
            async for message in queue_iter:
                async with message.process():
                    try:
                        event_data = json.loads(message.body)
                        await handler(event_data)
                    except Exception as e:
                        print(f"Error processing message from {queue_name}: {e}")


def add_queue_handler(queue_name, handler):
    """
    Add a queue handler to the dictionary for later startup.
    :param queue_name: Name of the RabbitMQ queue.
    :param handler: Async function to process messages from the queue.
    """
    queue_handlers[queue_name] = handler


async def start_all_queue_listeners():
    """
    Start listeners for all registered queues.
    """
    tasks = [
        asyncio.create_task(register_queue_listener(queue_name, handler))
        for queue_name, handler in queue_handlers.items()
    ]
    await asyncio.gather(*tasks)


async def process_game_added_event(
    event_data, vector_search: VectorSearch, embedding_generator: EmbeddingGenerator
):
    """
    Process the GameAddedEvent and extract the game name and rules.
    """
    try:
        event = GameAddedEvent(**event_data)
        rules = event.rules

        text = f"Rules for {event.gameName}: {' '.join([' '.join([rule.rule, rule.description]) for rule in rules])}"
        text_to_embed = " ".join(
            [query for query in generate_example_queries(event.gameName)]
        )

        embedding = embedding_generator.generate_embeddings([text_to_embed])

        vector_search.upload_data(
            text_to_embed=text_to_embed,
            info=text,
            embeddings=embedding[0],
            topic=get_rules_category(),
        )
        vector_search.upload_game_name(event.gameName)
        logging.info(f"New game {event.gameName} rules have been added")

    except Exception as e:
        print(f"Error parsing GameAddedEvent: {e}")
