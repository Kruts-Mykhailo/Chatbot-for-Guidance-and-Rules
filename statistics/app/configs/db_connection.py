import os
import psycopg2
import pandas as pd

# Database connection parameters
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5443")
DB_NAME = os.getenv("DB_NAME", "statistics")
DB_USER = os.getenv("DB_USER", "stats_admin")
DB_PASSWORD = os.getenv("DB_PASSWORD", "stats_adminpassword")

def get_connection():
    """Create and return a psycopg2 connection object."""
    print("Connecting to the database...")
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        print("Database connection established.")
        return conn
    except Exception as e:
        print("Error connecting to the database:", e)
        raise

def fetch_data():
    """
    Fetch player metrics data from the database and return it as a pandas DataFrame.
    """
    query = """
        SELECT
            player_player_id,
            total_games_played,
            total_wins ,
            total_losses,
            total_draws ,
            total_is_first ,
            avg_move_duration,
            total_weekdays_played,
            total_weekends_played,
            total_morning_plays ,
            total_afternoon_plays,
            total_evening_plays ,
            total_night_plays 
        FROM
            player_metrics
    """

    try:
        conn = get_connection()
        df = pd.read_sql_query(query, conn)
        conn.close()
        print("Data fetched successfully.")
        return df
    except Exception as e:
        print("Error fetching data:", e)
        raise

if __name__ == "__main__":
    df = fetch_data()
    print(df.head())
