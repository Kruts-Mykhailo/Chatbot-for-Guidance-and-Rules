import os
import pandas as pd
import joblib
from imblearn.over_sampling import SMOTE
from sklearn.model_selection import train_test_split, StratifiedKFold, GridSearchCV
from sklearn.metrics import accuracy_score, classification_report
from sklearn.ensemble import RandomForestClassifier

def train_model():
    """
    Train the churn prediction model with SMOTE to handle class imbalance
    and hyperparameter tuning using GridSearchCV.
    """
    training_csv = "./data/train/training_data.csv"
    if not os.path.exists(training_csv):
        raise FileNotFoundError(f"Training dataset not found at {training_csv}")

    print(f"Loading training dataset from '{training_csv}'...")
    df = pd.read_csv(training_csv)

    X = df[[
        "total_games_played",
        "weekend_ratio",
        "evening_ratio",
        "avg_game_duration",
        "total_weekdays_played",
        "total_weekends_played",
        "avg_moves_per_game"
    ]]
    y = df["churn"]  # Target variable (1 for churn, 0 for not churn)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, stratify=y, random_state=42
    )
    print(f"Training set size: {X_train.shape[0]}")
    print(f"Test set size: {X_test.shape[0]}")

    print("Applying SMOTE to balance the training dataset...")
    smote = SMOTE(random_state=42)
    X_train_resampled, y_train_resampled = smote.fit_resample(X_train, y_train)
    print(f"Resampled training set size: {X_train_resampled.shape[0]}")

    kf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

    param_grid = {
        'n_estimators': [50, 100, 200],
        'max_depth': [10, 20, None],
        'min_samples_split': [2, 5, 10],
        'min_samples_leaf': [1, 2, 4],
        'max_features': ['sqrt', 'log2', None]
    }

    print("Starting hyperparameter tuning with GridSearchCV...")
    grid_search = GridSearchCV(
        estimator=RandomForestClassifier(random_state=42),
        param_grid=param_grid,
        cv=kf,
        scoring='f1',
        n_jobs=-1
    )

    grid_search.fit(X_train_resampled, y_train_resampled)
    print("Best Parameters:", grid_search.best_params_)
    print("Best Cross-Validation Accuracy:", grid_search.best_score_)

    best_model = grid_search.best_estimator_
    print("Training the best model on the resampled training set...")
    best_model.fit(X_train_resampled, y_train_resampled)

    print("Evaluating the best model on the test set...")
    y_pred = best_model.predict(X_test)
    print("Test Set Evaluation:")
    print(f"Accuracy: {accuracy_score(y_test, y_pred):.2f}")
    print(classification_report(y_test, y_pred))

    model_path = "churn_model_smote.pkl"
    joblib.dump(best_model, model_path)
    print(f"Best model saved to '{model_path}'.")

if __name__ == "__main__":
    train_model()
