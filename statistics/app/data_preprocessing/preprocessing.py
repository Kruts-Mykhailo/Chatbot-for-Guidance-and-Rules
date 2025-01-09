import os
import pandas as pd
from datetime import datetime
from app.configs.db_connection import fetch_data

def preprocess_data(df):
    """
    Perform preprocessing steps on the raw DataFrame.
    """
    print("Starting preprocessing...")

    df.fillna(0, inplace=True)

    df["weekend_ratio"] = df["total_weekends_played"] / (
        df["total_weekends_played"] + df["total_weekdays_played"]
    )
    df["weekend_ratio"].fillna(0, inplace=True)  # Handle division by zero

    df["evening_ratio"] = df["total_evening_plays"] / df["total_games_played"]
    df["evening_ratio"].fillna(0, inplace=True)

    print("Preprocessing completed.")
    return df

def get_timestamped_filename(base_name="processed_player_metrics", extension="csv"):
    """
    Generate a filename with the current datetime included.

    Args:
        base_name (str): The base name of the file.
        extension (str): The file extension (e.g., "csv", "txt").

    Returns:
        str: A timestamped filename.
    """
    current_time = datetime.now().strftime("%Y%m%d_%H%M%S")  
    return f"{base_name}_{current_time}.{extension}"

if __name__ == "__main__":
    df = fetch_data()

    processed_df = preprocess_data(df)

    output_dir = "./data/test/"  

    timestamped_filename = get_timestamped_filename()
    processed_csv_path = os.path.join(output_dir, timestamped_filename)
    processed_df.to_csv(processed_csv_path, index=False)

    print(f"Processed data saved to '{processed_csv_path}'.")
