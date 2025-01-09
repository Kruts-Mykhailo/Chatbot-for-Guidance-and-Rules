from fastapi import FastAPI, HTTPException
import logging
from app.services.prediction_churn import predict_and_save_to_db

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

app = FastAPI()

@app.post("/predict")
async def trigger_prediction():
    """
    Endpoint to trigger the prediction process.
    """
    try:
        logging.info("Prediction process started...")
        predict_and_save_to_db()
        logging.info("Prediction process completed successfully.")
        return {"status": "success", "message": "Prediction process completed and data saved to the database."}
    except FileNotFoundError as e:
        logging.error(f"Error during prediction: {e}")
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logging.error(f"Error during prediction: {e}")
        raise HTTPException(status_code=500, detail="An error occurred during the prediction process.")
