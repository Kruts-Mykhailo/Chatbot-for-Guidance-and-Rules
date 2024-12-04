from typing import List
from psycopg2.extensions import connection
from chatbot.core.embeddings_generator.embeddings_generator_abstract import EmbeddingGenerator
from chatbot.core.embeddings_generator.embeddings_generator_factory import get_embedding_generator
from chatbot.core.vector_search.vector_search_abstract import VectorSearch
import numpy as np
import psycopg2
from psycopg2.extras import execute_batch, RealDictCursor
import os
from dotenv import load_dotenv

from chatbot.platform_guidance import guidance_loader

import logging


load_dotenv()

class PGVectorSearch(VectorSearch):
    def __init__(self) -> None:
        self.connection = None  # Initialize as None
        self.similarity_threshold: float = 0.5
        self.generator_type: str = "sentence_transformer"
        try:
            self.connection = self.connect()
            if self.connection:  # Proceed only if connection is successful
                self.create_game_names_table()
                self.ensure_guidance_data()
        except Exception as e:
            logging.error(f"Error during initialization: {e}")

    def connect(self) -> connection:
        try:
            conn = psycopg2.connect(
                dbname=os.getenv("DB_NAME"),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD"),
                host=os.getenv("DB_HOST"),
                port=os.getenv("DB_PORT"),
            )
            self.create_table()

            return conn
        
        except Exception as e:
            logging.error(f"Error connecting to PostgreSQL database: {e}")
            raise e

    def create_table(self) -> None:
        if self.connection:
            try:
                with self.connection.cursor() as cursor:
                    cursor.execute("""
                        CREATE TABLE IF NOT EXISTS vector_data (
                            id SERIAL PRIMARY KEY,
                            topic INT NOT NULL,
                            text TEXT NOT NULL,
                            embeddings VECTOR(768)
                        );
                    """)
                    self.connection.commit()
            except Exception as e:
                logging.error(f"Error creating table: {e}")

    def upload_data(self, texts: List[str], embeddings: np.ndarray, topic: int) -> None:
        if self.connection:
            try:
                with self.connection.cursor() as cursor:
                    sql = """
                        INSERT INTO vector_data (topic, text, embeddings)
                        VALUES (%s, %s, %s);
                    """
                    data = [
                        (topic, text, embedding.tolist()) for text, embedding in zip(texts, embeddings)
                    ]
                    execute_batch(cursor, sql, data)
                    self.connection.commit()
                    logging.info("Data uploaded successfully.")
            except Exception as e:
                logging.error(f"Error uploading data: {e}")

    def find_closest_text(self, query_embedding: np.ndarray) -> str:
        if self.connection:
            try:
                with self.connection.cursor(cursor_factory=RealDictCursor) as cursor:
                    cursor.execute("""
                        SELECT id, topic, text, embeddings <-> %s::vector AS distance
                        FROM vector_data
                        ORDER BY distance ASC
                        LIMIT 1;
                    """, (query_embedding.tolist()))
                    results = cursor.fetchall()
                    return results[0]['text']
            except Exception as e:
                print(f"Error finding closest text: {e}")
        return ""
    
    def get_category(self, query_embedding: np.ndarray) -> str:
        try:
            query_embedding = np.array(query_embedding).ravel()

            with self.connection.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("""
                    SELECT topic, embeddings <-> %s::vector AS distance
                    FROM vector_data
                    ORDER BY distance ASC
                    LIMIT 1;
                """, (query_embedding.tolist(),))
                
                result = cursor.fetchone()
                category = "unknown"

                if result and result["distance"] is not None:
                    # Check if the similarity is below the threshold
                    if result["distance"] >= self.similarity_threshold:
                        topic = result["topic"]
                        category =  guidance_loader.get_category_map().get(topic, category)
                    else:
                        logging.warning(f"Query similarity is too low: {result['distance']}. Categorizing as unrelated.")
                return category
        except Exception as e:
            logging.warning(f"Error identifying category: {e}")
            return "unknown"


    def contains_guidance_data(self) -> bool:
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("SELECT COUNT(*) FROM vector_data WHERE topic = %s;", (1,))
                result = cursor.fetchone()
                if result is None:
                    logging.error(f"Error checking for guidance data: Fetched None")
                    return False
                return result[0] > 0
        except Exception as e:
            logging.error(f"Error checking for guidance data: {e}")
            return False
        
    def upload_guidance_data(self) -> None:
            try:
                embedding_generator: EmbeddingGenerator = get_embedding_generator(self.generator_type)
                texts = guidance_loader.seed_data()
                topics = [1] * len(texts) 
                embeddings = embedding_generator.generate_embeddings(texts)

                with self.connection.cursor() as cursor:
                    sql = """
                        INSERT INTO vector_data (topic, text, embeddings)
                        VALUES (%s, %s, %s);
                    """
                    data = [
                        (topic, text, embedding.tolist()) for topic, text, embedding in zip(topics, texts, embeddings)
                    ]
                    execute_batch(cursor, sql, data)
                    self.connection.commit()
                    logging.info(f"Uploaded {len(data)} guidance records to the database.")
            except Exception as e:
                logging.error(f"Error uploading guidance data: {e}")
                
    def ensure_guidance_data(self) -> None:
        if not self.contains_guidance_data():
            logging.info("No guidance data found. Uploading from file...")
            self.upload_guidance_data()
        else:
            logging.info("Guidance data already exists in the database.")


    def create_game_names_table(self) -> None:
        """
        Creates the `game_names` table in the database if it doesn't exist.
        """
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS game_names (
                        id SERIAL PRIMARY KEY,
                        name TEXT NOT NULL UNIQUE
                    );
                """)
                self.connection.commit()
                logging.info("Table 'game_names' created successfully.")
        except Exception as e:
            logging.error(f"Error creating game_names table: {e}")

    def get_all_board_game_names(self) -> List[str]:
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("SELECT name FROM game_names;")
                rows = cursor.fetchall()
                return [row[0] for row in rows]
        except Exception as e:
            logging.error(f"Error retrieving board game names: {e}")
            return []

    def close(self) -> None:
        self.connection.close()



    