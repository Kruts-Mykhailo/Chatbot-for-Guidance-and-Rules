from pydantic import BaseModel
from typing import List

class PlayerMetricsBody(BaseModel):
    playerId: str
    gender: str
    age: int
    country: str
    city: str
    totalGamesPlayed: int
    totalWins: int
    totalLosses: int
    totalDraws: int
    totalIsFirst: int
    avgMoveDuration: float
    avgMoveAmount: float
    avgGameDuration: float
    totalWeekdaysPlayed: int
    totalWeekendsPlayed: int
    totalMorningPlays: int
    totalAfternoonPlays: int
    totalEveningPlays: int
    totalNightPlays: int

class PredictionsRequest(BaseModel):
    playerMetrics: List[PlayerMetricsBody]

class PlayerPredictionsBody(BaseModel):
    playerId: str
    churn: float
    firstMoveWinProbability: float
    playerClass: str

class PredictionsResponse(BaseModel):
    predictions: List[PlayerPredictionsBody]
