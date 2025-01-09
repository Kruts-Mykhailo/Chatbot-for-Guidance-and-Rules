import joblib
from sklearn.ensemble import RandomForestClassifier

class ChurnModel:
    """
    A class for the churn prediction model.
    """
    def __init__(self, n_estimators=50, max_depth=10, random_state=42):
        self.model = RandomForestClassifier(
            n_estimators=n_estimators,
            random_state=random_state
        )

    def train(self, X, y):
        """
        Train the model on the given data.
        """
        self.model.fit(X, y)

    def predict(self, X):
        """
        Predict churn for the given features.
        """
        return self.model.predict(X)

    def save_model(self, path="churn_model.pkl"):
        """
        Save the trained model to a file.
        """
        joblib.dump(self.model, path)
        print(f"Model saved to {path}.")

    def load_model(self, path="churn_model.pkl"):
        """
        Load a trained model from a file.
        """
        self.model = joblib.load(path)
        print(f"Model loaded from {path}.")
