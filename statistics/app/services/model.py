from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import pandas as pd

class PlayerMetricsModel:
    def __init__(self, data: pd.DataFrame):
        self.data = data
        self.churn_model = RandomForestClassifier()
        self.win_probability_model = RandomForestRegressor()
        self.classification_model = RandomForestClassifier()
        self.scaler = StandardScaler()
        self.train_models()

    def train_models(self):
        features = [
            "TotalGamesPlayed", "TotalWins", "TotalLosses", "AvgMoveDuration",
            "TotalWeekdaysPlayed", "TotalWeekendsPlayed", "TotalIsFirst", "TotalDraws"
        ]
        X = self.data[features]
        X_scaled = self.scaler.fit_transform(X)

        # Churn model
        self.data["Churn"] = self.data["Churn"].apply(lambda x: 1 if x >= 0.5 else 0)
        y_churn = self.data["Churn"]
        X_train, _, y_churn_train, _ = train_test_split(X_scaled, y_churn, test_size=0.2, random_state=42)
        self.churn_model.fit(X_train, y_churn_train)

        # Win probability model
        y_win_prob = self.data["FirstMoveWinProbability"]
        X_train, _, y_win_prob_train, _ = train_test_split(X_scaled, y_win_prob, test_size=0.2, random_state=42)
        self.win_probability_model.fit(X_train, y_win_prob_train)

        # Player classification model
        y_classification = self.data["PlayerClass"]
        X_train, _, y_classification_train, _ = train_test_split(X_scaled, y_classification, test_size=0.2, random_state=42)
        self.classification_model.fit(X_train, y_classification_train)

    def predict(self, player_metrics: pd.DataFrame):
        features = [
            "TotalGamesPlayed", "TotalWins", "TotalLosses", "AvgMoveDuration",
            "TotalWeekdaysPlayed", "TotalWeekendsPlayed", "TotalIsFirst", "TotalDraws"
        ]
        player_metrics.columns = [col[0].upper() + col[1:] if col[0].islower() else col for col in player_metrics.columns]

        X = player_metrics[features]
        X_scaled = self.scaler.transform(X)

        churn_probs = self.churn_model.predict_proba(X_scaled)[:, 1]

        win_probs = self.win_probability_model.predict(X_scaled)

        player_classes = self.classification_model.predict(X_scaled)

        return pd.DataFrame({
            "churn": churn_probs,
            "FirstMoveWinProbability": win_probs,
            "PlayerClass": player_classes
        })
