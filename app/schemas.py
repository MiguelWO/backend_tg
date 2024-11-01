from pydantic import BaseModel
from typing import List

class EmailContent(BaseModel):
    email_content: str

class PredictionResponse(BaseModel):
    is_phishing: bool
    confidence: float
    created_at: str
    risk_level: str


class PredictionsResponse(BaseModel):
    predictions: List[PredictionResponse]

