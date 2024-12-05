from typing import List

import numpy as np
from sentence_transformers import SentenceTransformer

from app.core.embedding.embeddings_generator_abstract import EmbeddingGenerator


class SentenceTransformerEmbeddingGenerator(EmbeddingGenerator):
    def __init__(self, model_name: str = "multi-qa-mpnet-base-cos-v1"):
        """
        Initializes the SentenceTransformer model.

        Args:
            model_name (str): The name of the model to load.
        """
        self.model = SentenceTransformer(model_name)

    def generate_embeddings(self, texts: List[str]) -> np.ndarray:
        """
        Generate embeddings using SentenceTransformer.

        Args:
            texts (List[str]): The list of texts to embed.

        Returns:
            np.ndarray: A NumPy array of embeddings.
        """
        return self.model.encode(texts, convert_to_numpy=True)
