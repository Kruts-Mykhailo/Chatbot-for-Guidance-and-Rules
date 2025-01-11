
from logging.config import dictConfig
from dotenv import load_dotenv
from app.configurations.logging_config import LOGGING_CONFIG

import os
import logging

from app.services.secrets.retriever_abstract import BaseRetriever

load_dotenv()
dictConfig(LOGGING_CONFIG)

class LocalSecretRetriever(BaseRetriever):
    def __init__(self) -> None:
        super().__init__()
    
    def get(self, variable_name: str, **kwargs) -> str:
        result = os.getenv(variable_name)
        if not result:
            logging.error(f"Failed to read value from {variable_name}")
            raise KeyError(f"Environment variable {variable_name} is not set or has no value.")
            
        return result
            

    
    