import logging
import os
from logging.config import dictConfig
from typing import List, Optional

import numpy as np
import psycopg2
from dotenv import load_dotenv
from psycopg2.extensions import connection
from psycopg2.extras import RealDictCursor, execute_batch

from app.configurations import guidance_loader
from app.configurations.logging_config import LOGGING_CONFIG
from app.core.embedding.embeddings_generator_abstract import EmbeddingGenerator
from app.core.embedding.embeddings_generator_factory import get_generator
from app.core.retrieval.vector_search_abstract import VectorSearch

dictConfig(LOGGING_CONFIG)

load_dotenv()


class PGVectorSearch(VectorSearch):
    def __init__(self) -> None:
        self.connection: Optional[connection] = None  # Initialize as None
        self.similarity_threshold: float = 0.3
        self.generator_type: str = "sentence_transformer"
        try:
            self.connection = self.connect()
            if self.connection:  # Proceed only if connection is successful
                self.create_table()
                self.create_game_names_table()
                self.upload_guidance_data()
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

            return conn

        except Exception as e:
            logging.error(f"Error connecting to PostgreSQL database: {e}")
            raise e

    def create_table(self) -> None:
        if self.connection:
            try:
                with self.connection.cursor() as cursor:
                    cursor.execute(
                        """
                        CREATE EXTENSION IF NOT EXISTS vector;
                        CREATE TABLE IF NOT EXISTS vector_data (
                            id SERIAL PRIMARY KEY,
                            topic INT NOT NULL,
                            text TEXT NOT NULL,
                            info TEXT,
                            embeddings VECTOR(768)
                        );
                    """
                    )
                    self.connection.commit()
                    logging.info("Table create process")
            except Exception as e:
                logging.error(f"Error creating table: {e}")

    def upload_data(
        self, text_to_embed: str, info: str, embeddings: np.ndarray, topic: int
    ) -> None:
        if self.connection:
            try:
                with self.connection.cursor() as cursor:
                    sql = """
                        INSERT INTO vector_data (topic, text, info, embeddings)
                        VALUES (%s, %s, %s, %s);
                    """
                    data = [(topic, text_to_embed, info, embeddings.tolist())]
                    execute_batch(cursor, sql, data)
                    self.connection.commit()
                    logging.info("Data uploaded successfully.")
            except Exception as e:
                logging.error(f"Error uploading data: {e}")

    def find_closest_text(self, query_embedding: np.ndarray) -> str:
        if self.connection:
            try:
                with self.connection.cursor(cursor_factory=RealDictCursor) as cursor:
                    cursor.execute(
                        """
                        SELECT id, topic, text, info, 1 - (embeddings <=> %s::vector) AS similarity
                        FROM vector_data
                        ORDER BY similarity DESC
                        LIMIT 1;
                    """,
                        (query_embedding.tolist()),
                    )
                    results = cursor.fetchall()
                    return results[0]["info"]
            except Exception as e:
                print(f"Error finding closest text: {e}")
        return ""

    def get_category(self, query_embedding: np.ndarray) -> str:
        if self.connection is None:
            logging.error("Connection is not established. Cannot create table.")
            return "unknown"

        try:
            query_embedding = np.array(query_embedding).ravel()

            with self.connection.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(
                    """
                    SELECT topic, 1 - (embeddings <=> %s::vector) AS similarity
                    FROM vector_data
                    ORDER BY similarity DESC
                    LIMIT 1;
                """,
                    (query_embedding.tolist(),),
                )

                result = cursor.fetchone()
                category = "unknown"

                if result and result["similarity"] is not None:
                    print(
                        f"The cosine similarity to closest category: {result['similarity']}"
                    )
                    if result["similarity"] > self.similarity_threshold:
                        category = result["topic"]
                return category
        except Exception as e:
            logging.warning(f"Error identifying category: {e}")
            return "unknown"

    def contains_guidance_data(self) -> bool:
        if self.connection is None:
            logging.error(
                "Connection is not established. Cannot identify guidance data presence."
            )
            return False
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(
                    "SELECT COUNT(*) FROM vector_data WHERE topic = %s;", (1,)
                )
                result = cursor.fetchone()
                if result is None:
                    logging.error(f"Error checking for guidance data: Fetched None")
                    return False
                return result[0] > 0
        except Exception as e:
            logging.error(f"Error checking for guidance data: {e}")
            return False

    def upload_guidance_data(self) -> None:
        if self.connection is None:
            logging.error("Connection is not established. Cannot upload guidance data.")
            return

        try:
            embedding_generator: EmbeddingGenerator = get_generator(self.generator_type)
            informations, texts_to_embed = guidance_loader.seed_data()
            topics = [1] * len(informations)
            embeddings = embedding_generator.generate_embeddings(texts_to_embed)

            with self.connection.cursor() as cursor:
                # Step 1: Create a temporary staging table
                cursor.execute(
                    """
                    CREATE TEMP TABLE staging_vector_data (
                        topic INT,
                        text TEXT,
                        info TEXT,
                        embeddings VECTOR(768)
                    );
                    """
                )

                # Step 2: Insert new guidance data into the staging table
                staging_data = [
                    (topic, text, info, embedding.tolist())
                    for topic, text, info, embedding in zip(
                        topics, texts_to_embed, informations, embeddings
                    )
                ]
                execute_batch(
                    cursor,
                    """
                    INSERT INTO staging_vector_data (topic, text, info, embeddings)
                    VALUES (%s, %s, %s, %s);
                    """,
                    staging_data,
                )

                # Step 3: Delete records in `vector_data` that are not in the staging table
                cursor.execute(
                    """
                    DELETE FROM vector_data
                    WHERE info NOT IN (SELECT info FROM staging_vector_data) AND topic = 1;
                    """
                )

                # Step 4: Update existing records in `vector_data`
                cursor.execute(
                    """
                    UPDATE vector_data
                    SET text = staging.text,
                        embeddings = staging.embeddings
                    FROM staging_vector_data staging
                    WHERE vector_data.info = staging.info;
                    """
                )

                # Step 5: Insert new records from the staging table into `vector_data`
                cursor.execute(
                    """
                    INSERT INTO vector_data (topic, text, info, embeddings)
                    SELECT staging.topic, staging.text, staging.info, staging.embeddings
                    FROM staging_vector_data staging
                    LEFT JOIN vector_data ON vector_data.text = staging.text
                    WHERE vector_data.text IS NULL;
                    """
                )

                self.connection.commit()
                logging.info(
                    f"Uploaded {len(staging_data)} guidance records to the database."
                )
        except Exception as e:
            logging.error(f"Error uploading guidance data: {e}")

    def create_game_names_table(self) -> None:
        if self.connection is None:
            logging.error(
                "Connection is not established. Cannot create table game_names."
            )
            return
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS game_names (
                        id SERIAL PRIMARY KEY,
                        name TEXT NOT NULL UNIQUE
                    );
                """
                )
                self.connection.commit()
                logging.info("Table 'game_names' created successfully.")
        except Exception as e:
            logging.error(f"Error creating game_names table: {e}")

    def get_all_board_game_names(self) -> List[str]:
        if self.connection is None:
            logging.error(
                "Connection is not established. Cannot retrieve board game names."
            )
            return []

        try:
            with self.connection.cursor() as cursor:
                cursor.execute("SELECT name FROM game_names;")
                rows = cursor.fetchall()
                return [row[0] for row in rows]
        except Exception as e:
            logging.error(f"Error retrieving board game names: {e}")
            return []

    def close(self) -> None:
        if self.connection is None:
            logging.error(
                "Connection was not established. Cannot close inexistent connection."
            )
            return
        self.connection.close()

    def upload_game_name(self, game_name: str) -> None:
        if self.connection is None:
            logging.error("Connection is not established. Cannot upload game name.")
            return

        try:
            with self.connection.cursor() as cursor:
                sql = """
                    INSERT INTO game_names(name)
                    VALUES (%s);
                """
                data = [(game_name,)]
                execute_batch(cursor, sql, data)
                self.connection.commit()
                logging.info(f"New game {game_name} added successfully.")
        except Exception as e:
            logging.error(f"Error uploading game name: {e}")
