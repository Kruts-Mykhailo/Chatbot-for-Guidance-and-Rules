import spacy
from typing import List

nlp = spacy.load("en_core_web_sm")

def get_game_entities(query: str) -> set[str]:
    doc = nlp(query.lower())
    tokens = {token.text for token in doc}
    entities = {ent.text.lower() for ent in doc.ents}
    query_terms = tokens.union(entities)
    return query_terms

def is_game_not_known(findings: set[str], known_games: List[str]) -> bool:
    for finding in findings:
        if finding.lower() in known_games:
            return False
    return True
