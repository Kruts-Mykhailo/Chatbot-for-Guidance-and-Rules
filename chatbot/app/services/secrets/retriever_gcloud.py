
from logging.config import dictConfig
from dotenv import load_dotenv
from app.configurations.logging_config import LOGGING_CONFIG
from google.cloud import secretmanager

import os
import logging

from app.services.secrets.retriever_abstract import BaseRetriever


dictConfig(LOGGING_CONFIG)

class GoogleCloudSecretRetriever(BaseRetriever):
    def __init__(self) -> None:
        self.project_id = "1038104239259"
        super().__init__()
    
    def get(self, variable_name: str, **kwargs) -> str:
        try:
            variable_name = variable_name.lower().replace("_", "-")
            client = secretmanager.SecretManagerServiceClient()
            secret_path = f"projects/{self.project_id}/secrets/{variable_name}/versions/latest"
            response = client.access_secret_version(request={"name": secret_path})
            secret_value = response.payload.data.decode("UTF-8")
            return secret_value
        except Exception as e:
            logging.error(f"Failed to read value from {variable_name}")
            raise Exception(f"Failed to retrieve secret: {e}")
            

    
    