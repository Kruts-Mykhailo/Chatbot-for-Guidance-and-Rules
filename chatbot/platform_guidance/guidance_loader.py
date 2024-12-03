import json
from typing import List, Dict
import os

PLATFORM_GUIDANCE_JSON="platform_guidance_v2.0.json"

def seed_data() -> List[str]:
    try:
        file_path = os.path.join(os.path.dirname(__file__), PLATFORM_GUIDANCE_JSON)
        with open(file_path, "r") as file:
            data = json.load(file)
        texts = [
            f"Guidance for {guidance['topic']}: " + " ".join(guidance["steps"])
            for guidance in data["guidance"]
        ]

        return texts
    except Exception as e:
        print(f"Error parsiong platform guidance file: {e}")
        return []

def get_topics() -> List[str]:
    try:
        with open(PLATFORM_GUIDANCE_JSON, "r") as file:
            data = json.load(file)
        return [guidance["topic"] for guidance in data["guidance"]]
    
    except Exception as e:
        print(f"Error parsiong platform guidance file: {e}")
        return []
    

def get_category_map() -> Dict[int, str]:
    return {
            1: "guidance",
            2: "rules",
        }