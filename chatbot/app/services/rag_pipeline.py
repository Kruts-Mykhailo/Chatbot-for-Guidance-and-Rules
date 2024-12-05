from typing import List

from app.core.embedding.embeddings_generator_abstract import EmbeddingGenerator
from app.core.language_models.llm_abstract import BaseLLM
from app.core.language_models.llm_factory import construct_prompt
from app.core.retrieval.vector_search_abstract import VectorSearch
from app.services.game_service import get_game_entities, is_game_not_known


def rag_pipeline(
    query: List[str],
    search: VectorSearch,
    embedding_generator: EmbeddingGenerator,
    model: BaseLLM,
) -> str:
    query_embedding = embedding_generator.generate_embeddings(query)

    category = search.get_category(query_embedding)

    retrieved_text: str = search.find_closest_text(query_embedding)

    if not retrieved_text or category == "unknown":
        return "Sorry, I can only answer questions about games on this platform or platform guidance."

    findings = get_game_entities(query[0])
    known_games = search.get_all_board_game_names()

    if category == "rules" and is_game_not_known(findings, known_games):
        return "Sorry, I do not know anything about this game. I am a chatbot that can only utilize the information from my knowledge base."

    base_prompt = construct_prompt(category, retrieved_text)

    response = model.generate(prompt=base_prompt)
    return response
