import pandas as pd

def load_and_prepare_data(csv_path: str):
    """
    Load and prepare the player statistics data from a CSV file.
    Args:
        csv_path (str): Path to the CSV file.

    Returns:
        pd.DataFrame: Prepared data.
    """
    data = pd.read_csv(csv_path)
    print("Normalized columns in player_metrics DataFrame:", data.columns.tolist())

    required_columns = [
        "PlayerId", "TotalGamesPlayed", "TotalWins", "TotalLosses",
        "AvgMoveDuration", "Churn"
    ]
    if not set(required_columns).issubset(data.columns):
        raise ValueError(f"CSV file must contain the following columns: {required_columns}")
    
    return data
