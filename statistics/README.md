## Features Used in the Churn Model

The model uses the following features for prediction:
- `total_games_played`
- `total_weekdays_played`
- `total_weekends_played`
- `avg_move_duration`
- `total_morning_plays`
- `total_evening_plays`
- `total_night_plays`

The target variable is `churn` (1 for churn, 0 for no churn).

---

## How to Use

### 1. Prerequisites

- **Python 3.12**
- Required Python libraries:
  - `pandas`
  - `joblib`
  - `sqlalchemy`
  - `fastapi`
  - `uvicorn`
  - `sklearn`
  - `imblearn`

Install all dependencies using:
```bash
pip install -r requirements.txt
```

### 2. Training the Model

#### Step 1: Prepare Training Data
Place the training dataset in the `data/train/` directory. The dataset should be a CSV file named `training_data_updated.csv` with the features mentioned above.

#### Step 2: Train the Model
Run the training script:
```bash
python -m app.services.training_churn
```

The trained model will be saved to `app/trained_models/churn/churn_model.pkl`.

---

### 4. Running the Prediction Service

#### Step 1: Start the FastAPI Server
Ensure you have the trained model file (`churn_model.pkl`) in `app/trained_models/churn/`. Start the FastAPI server using:
```bash
python -m app.main  
```

The API will be available at: `http://127.0.0.1:8000`

#### Step 2: Use the Prediction API
The `/predict` endpoint allows you to trigger the prediction pipeline.

##### Example Request
Send a POST request to `/predict` to fetch data, preprocess it, predict churn, and update the database.

Example using `curl`:
```bash
curl -X POST http://127.0.0.1:9090/predict
```