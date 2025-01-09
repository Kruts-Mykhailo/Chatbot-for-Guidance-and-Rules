import os
import pandas as pd
from datetime import datetime
from app.configs.db_connection import fetch_data

def preprocess_data(df):
    """
    Perform preprocessing steps on the raw DataFrame.
    """
    print("Starting preprocessing...")

    required_columns = [
        "player_id", "country", "city", "age", "gender",
        "total_games_played", "total_wins", "total_losses", "total_draws",
        "total_is_first", "avg_move_duration", "total_weekdays_played",
        "total_weekends_played", "total_morning_plays", "total_afternoon_plays",
        "total_evening_plays", "total_night_plays"
    ]
    for column in required_columns:
        if column not in df.columns:
            print(f"Missing column '{column}' detected. Adding default value 0.")
            df[column] = 0  # Default value for missing columns

    # Fill NaN values with 0
    df.fillna(0, inplace=True)

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


def save_processed_csv(df, output_dir="./data/test/", base_name="processed_player_metrics"):
    """
    Save the processed DataFrame to a timestamped CSV file.

    Args:
        df (pd.DataFrame): The processed DataFrame to save.
        output_dir (str): The directory where the CSV will be saved.
        base_name (str): The base name for the saved file.

    Returns:
        str: The path to the saved CSV file.
    """
    os.makedirs(output_dir, exist_ok=True)
    timestamped_filename = get_timestamped_filename(base_name=base_name, extension="csv")
    file_path = os.path.join(output_dir, timestamped_filename)
    df.to_csv(file_path, index=False)
    print(f"Processed data saved to '{file_path}'.")
    return file_path


if __name__ == "__main__":
    print("Fetching raw data from the database...")
    df = fetch_data()

    print("Processing data...")
    processed_df = preprocess_data(df)

    # Save the processed data to a CSV file
    processed_csv_path = save_processed_csv(processed_df)

    print(f"Processed data is saved at: {processed_csv_path}")
