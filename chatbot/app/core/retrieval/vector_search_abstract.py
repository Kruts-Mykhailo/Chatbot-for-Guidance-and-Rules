from abc import ABC, abstractmethod
from typing import Any, List

import numpy as np


class VectorSearch(ABC):
    """
    Abstract base class for vector search operations.
    """

    @abstractmethod
    def connect(self) -> Any:
        pass

    @abstractmethod
    def close(self) -> None:
        pass

    @abstractmethod
    def upload_data(
        self, text_to_embed: str, info: str, embeddings: np.ndarray, topic: int
    ) -> None:
        """
        Upload 1 record in vector database.
        """
        pass

    @abstractmethod
    def upload_game_name(self, game_name: str) -> None:
        pass

    @abstractmethod
    def find_closest_text(self, query_embedding: np.ndarray) -> str:
        pass

    @abstractmethod
    def get_category(self, query_embedding: np.ndarray) -> str:
        pass

    @abstractmethod
    def get_all_board_game_names(self) -> List[str]:
        pass
