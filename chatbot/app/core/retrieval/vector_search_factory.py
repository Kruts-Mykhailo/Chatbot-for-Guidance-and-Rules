from app.core.retrieval.vector_search_abstract import VectorSearch
from app.core.retrieval.vs_postgres_vector import PGVectorSearch


def get_solution(solution_type: str = "pgvector") -> VectorSearch:
    if solution_type == "pgvector":
        return PGVectorSearch()
    else:
        raise ValueError(f"Unknown vector search solution: {solution_type}")
