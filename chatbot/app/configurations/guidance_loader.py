import os
from typing import Dict, List, Tuple

from app.util.json_loader import load_from_file

PLATFORM_GUIDANCE_JSON = "platform_guidance_v2.0.json"


def seed_data() -> Tuple[List[str], List[str]]:
    try:
        file_path = os.path.join(os.path.dirname(__file__), PLATFORM_GUIDANCE_JSON)
        data = load_from_file(file_path)
        texts = [
            f"Guidance for {guidance["topic"]}: " + " ".join(guidance["steps"])
            for guidance in data["guidance"]
        ]
        infos = [" ".join(guidance["example_queries"]) for guidance in data["guidance"]]
        # infos = [
        #     prepare_for_embedding(guidance["topic"], guidance["keywords"])
        #     for guidance in data["guidance"]
        # ]

        return texts, infos
    except Exception as e:
        print(f"Error parsiong platform guidance file: {e}")
        return [], []


def get_topics() -> List[str]:
    try:
        file_path = os.path.join(os.path.dirname(__file__), PLATFORM_GUIDANCE_JSON)
        data = load_from_file(file_path)
        return [guidance["topic"] for guidance in data["guidance"]]

    except Exception as e:
        print(f"Error parsiong platform guidance file: {e}")
        return []


def prepare_for_embedding(topic: str, keywords: List[str]) -> str:
    """
    Preprocess topic and keywords into a single string for embedding.
    """
    return " ".join([topic.lower()] + [keyword.lower() for keyword in keywords])


def get_category_map() -> Dict[int, str]:
    return {
        1: "guidance",
        2: "rules",
    }
