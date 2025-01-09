import os
import pandas as pd
import joblib
from sqlalchemy import create_engine, text
from app.configs.db_connection import fetch_data
from app.data_preprocessing.preprocessing import preprocess_data, save_processed_csv
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

DB_URL = os.getenv("DB_URL", "localhost:5443")
DB_NAME = os.getenv("DB_NAME", "statistics")
DB_USER = os.getenv("DB_USER", "stats_admin")
DB_PASSWORD = os.getenv("DB_PASSWORD", "stats_adminpassword")
TABLE_NAME = "player_predicitons"

def predict_and_save_to_db():
    """
    Fetch data from the database, preprocess it, save to a CSV file,
    reload the CSV file, make predictions using the trained model, 
    and update the database with predictions.
    """
    model_path = "./app/trained_models/churn/churn_model.pkl"

    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Trained model not found at {model_path}")
    logging.info(f"Loading model from '{model_path}'...")
    model = joblib.load(model_path)

    logging.info("Fetching data from the database...")
    raw_data = fetch_data()

    logging.info("Preprocessing data...")
    df = preprocess_data(raw_data)

    output_dir = "./data/processed/"
    os.makedirs(output_dir, exist_ok=True)
    processed_csv_path = save_processed_csv(df, output_dir=output_dir, base_name="preprocessed_player_metrics")
    logging.info(f"Preprocessed data saved to '{processed_csv_path}'.")

    logging.info("Reloading preprocessed data from the saved CSV...")
    df = pd.read_csv(processed_csv_path)

    features = [
        "total_games_played",
        "total_weekdays_played",
        "total_weekends_played",
        "avg_move_duration",
        "total_morning_plays",
        "total_evening_plays",
        "total_night_plays"
    ]

    try:
        X = df[features]
    except KeyError as e:
        logging.error(f"Missing required features: {e}")
        return

    logging.info("Making predictions...")
    df["churn"] = model.predict(X)

    # Placeholder values for other metrics
    df["first_move_win_probability"] = 0.5
    df["player_class"] = "BEGINNER"

    predictions_to_save = df[["player_player_id", "churn", "first_move_win_probability", "player_class"]]
    predictions_to_save.rename(columns={"player_id": "player_player_id"})

    logging.info(f"Saving predictions to the '{TABLE_NAME}' table...")
    logging.info(f"Predictions to save:\n{predictions_to_save}")

    save_predictions_to_db(predictions_to_save)


def save_predictions_to_db(predictions_df):
    """
    Save or update predictions in the 'player_predictions' table.
    """
    db_url = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_URL}/{DB_NAME}"
    engine = create_engine(db_url)
   


    with engine.connect() as connection:
        with connection.begin(): 
            for _, row in predictions_df.iterrows():
                try:
                    player_id = row["player_player_id"]
                    churn = row["churn"]
                    first_move_win_probability = row["first_move_win_probability"]
                    player_class = row["player_class"]

                    result = connection.execute(
                        text(f"SELECT 1 FROM {TABLE_NAME} WHERE player_player_id = :player_id"),
                        {"player_id": player_id}
                    ).fetchone()

                    if result:
                        # Update all columns
                        connection.execute(
                            text(f"""
                                UPDATE {TABLE_NAME}
                                SET churn = :churn,
                                    first_move_win_probability = :first_move_win_probability,
                                    player_class = :player_class
                                WHERE player_player_id = :player_id
                            """),
                            {
                                "player_id": player_id,
                                "churn": churn,
                                "first_move_win_probability": first_move_win_probability,
                                "player_class": player_class
                            }
                        )
                    else:
                        # Insert a new row
                        connection.execute(
                            text(f"""
                                INSERT INTO {TABLE_NAME} (player_player_id, churn, first_move_win_probability, player_class)
                                VALUES (:player_id, :churn, :first_move_win_probability, :player_class)
                            """),
                            {
                                "player_id": player_id,
                                "churn": churn,
                                "first_move_win_probability": first_move_win_probability,
                                "player_class": player_class
                            }
                        )
                except Exception as e:
                    logging.error(f"Error saving prediction for player_id {row['player_player_id']}: {e}")
        logging.info("Predictions saved successfully.")


if __name__ == "__main__":
    predict_and_save_to_db()
