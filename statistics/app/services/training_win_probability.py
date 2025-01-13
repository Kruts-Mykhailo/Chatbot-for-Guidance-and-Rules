import os
import pandas as pd
import joblib
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import mean_squared_error, r2_score

def train_win_probability_model():
    """
    Train the win probability estimation model on preprocessed data.
    """
    # Path to preprocessed data
    training_csv = "./data/train/training_data_updated.csv"
    if not os.path.exists(training_csv):
        raise FileNotFoundError(f"Training dataset not found at {training_csv}")

    print(f"Loading training dataset from '{training_csv}'...")
    df = pd.read_csv(training_csv)

    # Features and target for win probability estimation
    features = [
        "total_games_played",
        "total_weekdays_played",
        "total_weekends_played",
        "avg_move_duration",
        "total_morning_plays",
        "total_evening_plays",
        "total_night_plays"
    ]
    target = "first_move_win_probability"

    X = df[features]
    y = df[target]

    # Split into train and test sets
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    print(f"Training set size: {X_train.shape[0]}")
    print(f"Test set size: {X_test.shape[0]}")

    # Define the model
    model = RandomForestRegressor(random_state=42)

    # Hyperparameter tuning with GridSearchCV
    param_grid = {
        'n_estimators': [50, 100, 200],
        'max_depth': [10, 20, None],
        'min_samples_split': [2, 5, 10],
        'min_samples_leaf': [1, 2, 4],
        'max_features': ['sqrt', 'log2', None]
    }

    print("Starting hyperparameter tuning with GridSearchCV...")
    grid_search = GridSearchCV(
        estimator=model,
        param_grid=param_grid,
        cv=5,
        scoring='neg_mean_squared_error',
        n_jobs=-1
    )

    grid_search.fit(X_train, y_train)
    print("Best Parameters:", grid_search.best_params_)
    print("Best Cross-Validation Score:", grid_search.best_score_)

    # Train the best model
    best_model = grid_search.best_estimator_
    print("Training the best model on the training set...")
    best_model.fit(X_train, y_train)

    # Evaluate the model on the test set
    print("Evaluating the model on the test set...")
    y_pred = best_model.predict(X_test)
    print(f"Mean Squared Error: {mean_squared_error(y_test, y_pred):.4f}")
    print(f"R-squared: {r2_score(y_test, y_pred):.4f}")

    # Save the model
    model_path = "./app/trained_models/win_probability_model.pkl"
    joblib.dump(best_model, model_path)
    print(f"Model saved to '{model_path}'.")

if __name__ == "__main__":
    train_win_probability_model()
