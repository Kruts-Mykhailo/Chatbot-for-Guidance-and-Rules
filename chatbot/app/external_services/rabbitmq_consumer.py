import asyncio
import json
import os

from aio_pika import connect
from dotenv import load_dotenv

from app.core.retrieval.vector_search_abstract import VectorSearch
from app.external_services.event_model import GameAddedEvent

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


async def process_game_added_event(event_data, vector_search: VectorSearch):
    """
    Process the GameAddedEvent and extract the game name and rules.
    """
    try:
        event = GameAddedEvent(**event_data)

        print(f"Game received: {event.gameName}")
        for rule in event.rules:
            print(f"Rule: {rule.rule}, Description: {rule.description}")

    except Exception as e:
        print(f"Error parsing GameAddedEvent: {e}")
