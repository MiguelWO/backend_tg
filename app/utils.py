from io import BytesIO
import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.models import Sequential
from keras.layers import Dense, Embedding, LSTM
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from keras.layers import TFSMLayer
import pickle
# Importar wordcloud
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from app.email_parser import extract_email_content

# Importar el modelo  
# model_best = keras.models.load_model('./models/tuned_best_model.pkl')
# model_mlp = keras.models.load_model('./models/tuned_mlp_model.pkl')

# model_best = Sequential([
#     TFSMLayer('./models/tuned_best_model.pkl', call_endpoint='serving_default')
# ])

# Load model .pkl
# 

# model_mlp = Sequential([
#     TFSMLayer('./models/tuned_mlp_model.pkl', call_endpoint='serving_default')
# ])

import os
print(os.getcwd()) 

# with open(r'app/models/tuned_best_model.pkl', 'rb') as file:
#     model_best = pickle.load(file)

# model_best = model_best.estimator

# with open('app/models/tuned_mlp_model.pkl', 'rb') as file:
#     model_mlp = pickle.load(file)

# model_mlp = model_mlp.estimator

# keras_model = tf.keras.models.load_model('app/models/phishing_model_keras.keras')

# Cargar el modelo
# model = keras_model

# Descargar recursos de nltk
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('wordnet')

# Crear un conjunto de palabras vacías en inglés
stop_words = set(stopwords.words('english'))

custom_stopwords = {"uwaterloo", "ethz", "adobe", "photoshop", "ca", "minimal", "mail", "project", "stat", "math", "mailing", "posting", "read", "list", "commented", "provide", "reproducible"}  # Añade más palabras aquí si es necesario
stop_words = stop_words.union(custom_stopwords)

# Load the tokenizer
with open('./app/models/tokenizer.pkl', 'rb') as handle:
    tokenizer = pickle.load(handle)


# Función para procesar texto: eliminar stopwords, tokenizar y lematizar
def process_text(text):
    tokens = word_tokenize(text.lower())  # Convertir a minúsculas y tokenizar
    tokens = [t for t in tokens if t.isalnum()]  # Eliminar puntuación
    tokens = [t for t in tokens if t not in stop_words]  # Eliminar stopword
    # IsAlpha
    tokens = [t for t in tokens if t.isalpha()]
    return ' '.join(tokens)
    

def preprocess_content(content, for_wordcloud=False):
    """
    Preprocesses email content for either word cloud generation or prediction.
    """
    content = extract_email_content(content)
    print(content)

    # Ensure email_content is a string
    if isinstance(content, bytes):
        content = content.decode('utf-8')

    # print(content)

    text_to_process = f"{content['sender']} {content['receiver']} {content['subject']} {content['body']}"
    # print(text_to_process)

    # Tokenize and lemmatize
    words = process_text(text_to_process)
    print(words)

    if for_wordcloud:
        return words
    
    # Tokenize and pad for prediction
    headers_clean = ' '.join(words.split())
    print(headers_clean)
    headers_sequence = tokenizer.texts_to_sequences([headers_clean])
    print(headers_sequence)
    headers_padded = pad_sequences(headers_sequence, maxlen=100)
    print(headers_padded)
    return headers_padded

def worldcloud(email_content):
    """
    Generates a word cloud image from email content.
    """
    # Ensure email_content is a string
    if isinstance(email_content, bytes):
        email_content = email_content.decode('utf-8')
    
    # Preprocess specifically for word cloud
    data = preprocess_content(email_content, for_wordcloud=True)

    # Generate WordCloud
    wordcloud = WordCloud(
        width=800, 
        height=800, 
        background_color='white', 
        stopwords=stop_words, 
        min_font_size=10
    ).generate(data)
    
    return wordcloud



def predict_phishing(email_content, model_path):
    """
    Predict if an email is phishing or not using a pre-trained model.
    """
    # Load the model
    try:
        model = load_model(model_path)
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Error loading model: {e}")
    
    # Preprocess the email content for prediction
    preprocessed_content = preprocess_content(email_content)
    print(preprocessed_content)

    # Generate prediction
    prediction = model.predict(preprocessed_content)
    confidence = float(prediction[0][0])  # Assuming binary classification
    # print(prediction)
    
    return {
        'email_content': email_content,
        'is_phishing': confidence > 0.3,  # True if confidence is greater than 0.5
        'confidence': confidence
    }

def load_model(path):
    """
    Load a Keras model from a given path.
    """
    print(os.getcwd())
    try:
        return keras.models.load_model(path)
    except Exception as e:
        raise FileNotFoundError(f"Error loading model at {path}: {e}")

