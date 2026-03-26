from pydantic import BaseModel
from datetime import datetime

class SignalCreate(BaseModel):
    source: str
    content: str


class SignalResponse(BaseModel):
    id: int
    source: str
    timestamp: datetime
    summary: str
    type: str
    impact_score: float
    urgency_score: float
    cluster_id: str

    class Config:
        from_attributes = True


class InsightResponse(BaseModel):
    id: int
    cluster_id: str
    summary: str
    status: str

    class Config:
        from_attributes = True