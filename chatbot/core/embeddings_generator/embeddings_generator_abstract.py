
from abc import ABC, abstractmethod
from typing import List
import numpy as np

class EmbeddingGenerator(ABC):
    """
    Abstract base class for embedding generation.
    """

    @abstractmethod
    def generate_embeddings(self, texts: List[str]) -> np.ndarray:
        """
        Generate embeddings for a list of texts.

        Args:
            texts (List[str]): The list of texts to embed.

        Returns:
            np.ndarray: A NumPy array of embeddings.
        """
        pass