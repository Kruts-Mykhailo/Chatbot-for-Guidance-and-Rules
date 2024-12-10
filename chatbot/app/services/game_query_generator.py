from typing import List

from app.external_services.event_model import GameRule


def generate_example_queries(game_name: str) -> List[str]:
    """
    Generate example queries about how to play a game and its rules.

    :param game_name: The name of the game.
    :param rules: A list of GameRule objects representing the game's rules.
    :return: A list of example queries.
    """
    queries = []

    # General queries about how to play the game
    queries.append(f"How do I play {game_name}?")
    queries.append(f"What are the rules for {game_name}?")
    queries.append(f"Can you explain the rules of {game_name}?")
    queries.append(f"How do I start playing {game_name}?")
    queries.append(f"What is the objective of {game_name}?")
    return queries
