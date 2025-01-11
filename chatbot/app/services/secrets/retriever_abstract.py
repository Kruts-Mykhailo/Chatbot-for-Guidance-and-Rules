from abc import ABC, abstractmethod


class BaseRetriever(ABC):
    """
    Abstract base class for retrieving secrets.
    """

    @abstractmethod
    def get(self, variable_name: str, **kwargs) -> str:
        """
        Get informatino from a requested variable

        :param variable_name: name of the variable to retrieve information from.
        :param kwargs: Additional arguments.
        :return: The generated response as a string.
        """
        pass
