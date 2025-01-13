from pydantic import BaseModel
from typing import List

class PlayerMetricsBody(BaseModel):
    PlayerId: str
    TotalGamesPlayed: int
    TotalWins: int
    TotalLosses: int
    AvgMoveDuration: float
    TotalWeekdaysPlayed: int
    TotalWeekendsPlayed: int
    TotalIsFirst: int
    TotalDraws: int

class PredictionsRequest(BaseModel):
    playerMetrics: List[PlayerMetricsBody]

class PlayerPredictionsBody(BaseModel):
    playerId: str
    churn: float
    firstMoveWinProbability: float
    playerClass: str

class PredictionsResponse(BaseModel):
    predictions: List[PlayerPredictionsBody]
