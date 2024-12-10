from typing import List, Optional

from pydantic import BaseModel


class GameRule(BaseModel):
    rule: str
    description: str


class GameAddedEvent(BaseModel):
    gameName: str
    description: Optional[str] = None
    price: Optional[float] = None
    currency: Optional[str] = None
    maxLobbyPlayersAmount: Optional[int] = None
    frontendUrl: Optional[str] = None
    backendApiUrl: Optional[str] = None
    gameImageUrl: Optional[str] = None
    rules: List[GameRule] = []
