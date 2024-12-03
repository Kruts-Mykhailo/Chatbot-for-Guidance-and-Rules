from chatbot.embeddings_generator.eg_sentence_transformer import SentenceTransformerEmbeddingGenerator
from chatbot.embeddings_generator.embeddings_generator_abstract import EmbeddingGenerator

def get_embedding_generator(generator_type: str = "sentence_transformer") -> EmbeddingGenerator:
    """
    Factory function to get the embedding generator.

    Args:
        generator_type (str): The type of embedding generator to use.
                              Options: "sentence_transformer"...

    Returns:
        EmbeddingGenerator: The embedding generator instance.
    """
    if generator_type == "sentence_transformer":
        return SentenceTransformerEmbeddingGenerator()
    else:
        raise ValueError(f"Unknown embedding generator type: {generator_type}")