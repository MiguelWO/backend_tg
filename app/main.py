import base64
from datetime import datetime
from io import BytesIO
from fastapi import Depends, FastAPI, UploadFile, File, Form, HTTPException
from typing import List
from fastapi.responses import JSONResponse, StreamingResponse
from matplotlib import pyplot as plt
from pydantic import BaseModel
from models import predict_phising, worldcloud
import uvicorn
from schemas import PredictionResponse, EmailContent, PredictionsResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from models_db import SessionLocal, engine, Prediction, Model



app = FastAPI(
    title='Phishing Email Detector',
    description='API for Phishing Email Detector',
    version='0.1',
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post('/predict', response_model=PredictionResponse)
async def predict(email_content: EmailContent, db: Session = Depends(get_db)):
    """
    Predict if an email is phishing or not

    - **email_content**: The content of the email

    Returns:
    - **is_phishing**: Whether the email is phishing or not
    - **confidence**: The confidence of the model in the prediction

    """
    try: 
        prediction = predict_phising(email_content.email_content)

        is_phishing = bool(prediction['is_phishing'])
        confidence = float(prediction['confidence'])
        date = datetime.now()

        db_prediction = Prediction(email_content=email_content.email_content, prediction=is_phishing, confidence=confidence, created_at=date)

        db.add(db_prediction)
        db.commit()
        db.refresh(db_prediction)

        response = PredictionResponse(
            is_phishing=is_phishing,
            confidence=confidence,
            created_at=date,
            risk_level='High' if confidence > 0.5 else 'Low'
        )

        return response
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post('/generate_wordcloud')
async def generate_wordcloud(email_content: EmailContent, db: Session = Depends(get_db)):
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



@app.get('/predictions', response_model=PredictionsResponse)
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
                'is_phishing': prediction.prediction,
                'confidence': prediction.confidence
            })

        # print(response)

        return {'predictions': response}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))



@app.post('/predict_file', response_model=PredictionResponse)
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
    prediction = predict_phising(email_content)
    return prediction

@app.post('/predict_form', response_model=PredictionResponse)
async def predict_form(email_content: str = Form(...)):
    """
    Predict if an email is phishing or not

    - **email_content**: The content of the email

    Returns:
    - **is_phishing**: Whether the email is phishing or not
    - **confidence**: The confidence of the model in the prediction

    """
    prediction = predict_phising(email_content)
    return prediction

@app.get('/')
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


@app.post('/restore')
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



if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
