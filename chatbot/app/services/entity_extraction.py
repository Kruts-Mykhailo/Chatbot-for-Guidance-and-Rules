from typing import List

import stanza

# Load Stanza model (only required once)
stanza.download("en")
nlp = stanza.Pipeline(lang="en", processors="tokenize,ner")

def get_game_entities(query: str) -> set[str]:
    doc = nlp(query.lower())
    tokens = {word.text for sentence in doc.sentences for word in sentence.words}
    entities = {ent.text.lower() for ent in doc.ents}
    query_terms = tokens.union(entities)
    return query_terms



def is_game_not_known(findings: set[str], known_games: List[str]) -> bool:
    for finding in findings:
        if finding.lower() in known_games:
            return False
    return True
