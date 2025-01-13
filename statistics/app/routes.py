from fastapi import APIRouter, HTTPException
from app.models.models import PredictionsRequest, PredictionsResponse, PlayerPredictionsBody
from app.services.model import PlayerMetricsModel
import pandas as pd

router = APIRouter()

data = pd.read_csv("data/players_statistics.csv")
player_metrics_model = PlayerMetricsModel(data)

@router.post("/predict", response_model=PredictionsResponse)
def predict(request: PredictionsRequest):
    player_metrics = pd.DataFrame([p.dict() for p in request.playerMetrics])

    try:
        predictions = player_metrics_model.predict(player_metrics)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    response_data = [
        PlayerPredictionsBody(
            playerId=row["PlayerId"],
            churn=row["churn"],
            firstMoveWinProbability=row["FirstMoveWinProbability"],
            playerClass=row["PlayerClass"]
        )
        for row in player_metrics.assign(**predictions).to_dict(orient="records")
    ]

    return PredictionsResponse(predictions=response_data)
