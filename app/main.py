import base64
from datetime import datetime
from io import BytesIO
from fastapi import Depends, FastAPI, UploadFile, File, Form, HTTPException
from typing import List
from fastapi.responses import JSONResponse, StreamingResponse
from matplotlib import pyplot as plt
from pydantic import BaseModel
from app.utils import worldcloud, predict_phishing
import uvicorn
from app.schemas import PredictionResponse, EmailContent, PredictionsResponse, ModelResponse, ModelsResponse, EmailContentWordCloud
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from app.models_db import SessionLocal, engine, Prediction, Model, initialize_models
# Import router
from fastapi import APIRouter
import os



app = FastAPI(
    title='Phishing Email Detector',
    description='API for Phishing Email Detector',
    version='0.1',
)

# Create a router
router = APIRouter(prefix="/api", tags=["api"])

def get_db():
    db = SessionLocal()
    try:
        initialize_models(db)
        yield db
    finally:
        db.close()

origins = [
    "http://localhost:3000",
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:8080",
    "http://localhost:5000",
    "http://localhost:4200",
    "https://frontend-tg.vercel.app"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/ping")
def pong():
    return {"ping": "pong!"}

@router.post('/predict', response_model=PredictionResponse)
async def predict(
    email_content: EmailContent,
    db: Session = Depends(get_db)):
    """
    Predict if an email is phishing or not

    - **email_content**: The content of the email and the model name

    Returns:
    - **is_phishing**: Whether the email is phishing or not
    - **confidence**: The confidence of the model in the prediction

    """
    try:
        db_model = db.query(Model).filter(Model.display_name == email_content.model_name).first()
        if not db_model:
            raise HTTPException(status_code=404, detail='Model not found')
        
        model_path = f'./app/models/{db_model.name}.{db_model.extension}'

        prediction = predict_phishing(email_content.email_content, model_path)

        is_phishing = bool(prediction['is_phishing'])
        confidence = float(prediction['confidence'])
        date = datetime.now()
        model_id = db_model.id

        db_prediction = Prediction(
            email_content=email_content.email_content,
            prediction=is_phishing,
            confidence=confidence,
            model_id=model_id,
            created_at=date
        )

        db.add(db_prediction)
        db.commit()

        response = PredictionResponse(
            is_phishing=is_phishing,
            confidence=confidence,
            created_at=date,
            risk_level='High' if confidence > 0.8 else 'Medium' if confidence > 0.3 else 'Low',
            model_id = model_id
        )

        return response
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post('/generate_wordcloud')
async def generate_wordcloud(email_content: EmailContentWordCloud, db: Session = Depends(get_db)):
    """
    Generate a wordcloud for the email content

    - **email_content**: The content of the email

    Returns:
    - **wordcloud**: The wordcloud image
    """
    try:
        wordcloud = worldcloud(email_content.email_content)

        # print('wordcloud', wordcloud)

        buffer = BytesIO()

        # print('buffer', buffer)
        
        wordcloud.to_image().save(buffer, format='PNG')
        buffer.seek(0)

        image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')

        return { 'wordcloud': image_base64 }

    except Exception as e:
        # print('error', e)
        raise HTTPException(status_code=400, detail=str(e))



@router.get('/predictions', response_model=PredictionsResponse)
async def get_predictions(db: Session = Depends(get_db)):
    """
    Get all predictions

    Returns:
    - **predictions**: A list of all predictions
    """
    try:
        predictions = db.query(Prediction).all()
        # for prediction in predictions:
        #     print("Content_email",prediction.email_content)
        #     print("prediction", prediction.prediction)
        #     print("confidence",prediction.confidence)

        response = []
        for prediction in predictions:
            response.append({
                'email_content': prediction.email_content,
                'is_phishing': prediction.prediction,
                'confidence': prediction.confidence,
                'created_at': prediction.created_at,
                'risk_level': 'High' if prediction.confidence > 0.8 else 'Medium' if prediction.confidence > 0.5 else 'Low',
                'model_id': prediction.model_id
            })

        # print(response)

        return {'predictions': response}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))



@router.post('/predict_file', response_model=PredictionResponse)
async def predict_file(file: UploadFile = File(...)):
    """
    Predict if an email is phishing or not
    
    - **file**: The file containing the email content
    
    Returns:
    - **is_phishing**: Whether the email is phishing or not
    - **confidence**: The confidence of the model in the prediction
    """

    content = await file.read()
    email_content = content.decode('utf-8')
    prediction = predict_phishing(email_content)
    return prediction

@router.post('/predict_form', response_model=PredictionResponse)
async def predict_form(email_content: str = Form(...)):
    """
    Predict if an email is phishing or not

    - **email_content**: The content of the email

    Returns:
    - **is_phishing**: Whether the email is phishing or not
    - **confidence**: The confidence of the model in the prediction

    """
    prediction = predict_phishing(email_content)
    return prediction


# Get all the display name of the models
@router.get('/models/names', response_model=List[str])
async def get_models(db: Session = Depends(get_db)):
    """
    Get all available models

    Returns:
    - **models**: A list of all available models
    """
    try:
        models = db.query(Model).all()
        response = [model.display_name for model in models]
        return response
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
# Get all models and thier ids
@router.get('/models/ids', response_model=List[ModelResponse])
async def get_models(db: Session = Depends(get_db)):
    """
    Get all available models

    Returns:
    - **models**: A list of all available models
    """
    try:
        models = db.query(Model).all()
        return models
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Get all the models
@router.get('/models', response_model=List[ModelResponse])
async def get_models(db: Session = Depends(get_db)):
    """
    Get all available models

    Returns:
    - **models**: A list of all available models
    """
    try:
        models = db.query(Model).all()
        return models
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
# Get a specific model
@router.get('/models/{model_id}', response_model=ModelResponse)
async def get_model(model_id: int, db: Session = Depends(get_db)):
    """
    Get a specific model

    - **model_id**: The ID of the model

    Returns:
    - **model**: The model
    """
    try:
        model = db.query(Model).filter(Model.id == model_id).first()
        if not model:
            raise HTTPException(status_code=404, detail='Model not found')
        return model
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get('/')
async def index():
    return {'text': 'Hello World!'}

# Error handling
@app.exception_handler(Exception)
async def validation_exception_handler(request, exc):
    """
    Error handler for validation exceptions
    
    Returns:
    - **message**: The error message
    """
    
    return JSONResponse(
        status_code=400,
        content={"message": str(exc)},
    )


@router.post('/restore')
async def restore(db: Session = Depends(get_db)):
    """
    Restore the database

    Returns:
    - **message**: The result of the operation
    """
    try:
        Model.metadata.drop_all(bind=engine)
        Model.metadata.create_all(bind=engine)
        return {'message': 'Database restored'}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


app.include_router(router)


if __name__ == '__main__':
    PORT = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host='0.0.0.0', port= PORT)
