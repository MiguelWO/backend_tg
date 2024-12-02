from datetime import datetime
from pydantic import BaseModel
from typing import List

class EmailContent(BaseModel):
    email_content: str
    model_name : str

class EmailContentWordCloud(BaseModel):
    email_content: str

    
class PredictionResponse(BaseModel):
    is_phishing: bool
    confidence: float
    created_at: datetime
    risk_level: str
    model_id : int


class PredictionsResponse(BaseModel):
    predictions: List[PredictionResponse]


class ModelResponse(BaseModel):
    id: int
    name: str
    extension: str
    display_name: str
    
    class config:
        orm_mode = True

class ModelsResponse(BaseModel):
    models: List[ModelResponse]



