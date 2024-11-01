import pytest 
from fastapi.testclient import TestClient
from app.main import app
import sys
import os

# Agrega la carpeta principal al PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

client = TestClient(app)

def test_predict():
    response = client.post(
        "/predict",
        json={"email_content": "This is a test email content"}
    )
    assert response.status_code == 200
    assert "is_phishing" in response.json()
    assert "confidence" in response.json()

def test_get_predictions():
    response = client.get("/predictions")
    assert response.status_code == 200
    assert "predictions" in response.json()
    assert isinstance(response.json()["predictions"], list)

def test_predict_file():
    file_content = b"This is a test email content"
    response = client.post(
        "/predict_file",
        files={"file": ("test_email.txt", file_content)}
    )
    assert response.status_code == 200
    assert "is_phishing" in response.json()
    assert "confidence" in response.json()

def test_predict_form():
    response = client.post(
        "/predict_form",
        data={"email_content": "This is a test email content"}
    )
    assert response.status_code == 200
    assert "is_phishing" in response.json()
    assert "confidence" in response.json()

def test_integration_flow():
    # Enviar el correo por el endpoint de predicción
    response = client.post(
        "/predict",
        json={"email_content": "This is a test email content"}
    )
    assert response.status_code == 200
    assert "is_phishing" in response.json()
    assert "confidence" in response.json()

    # Obtener todas las predicciones
    response = client.get("/predictions")
    assert response.status_code == 200
    predictions = response.json()["predictions"]
    assert len(predictions) > 0  # Debe haber al menos una predicción
    assert "is_phishing" in predictions[0]
    assert "confidence" in predictions[0]