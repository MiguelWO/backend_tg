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

keras_model = tf.keras.models.load_model('app/models/phishing_model_keras.keras')

# Cargar el modelo
model = keras_model

# Descargar recursos de nltk
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')

# Crear un conjunto de palabras vacías en inglés
stop_words = set(stopwords.words('english'))

tokenizer = Tokenizer(num_words=5000)

def preprocess_content(content, for_wordcloud=False):
    """
    Preprocesses email content for either word cloud generation or prediction.
    """
    # Lowercase, tokenize, and remove stopwords
    words = [
        word for word in word_tokenize(content.lower()) if word.isalpha() and word not in stop_words
    ]
    
    if for_wordcloud:
        # Return a single string for WordCloud generation
        return ' '.join(words)
    
    # Tokenize and pad for prediction model
    headers_clean = ' '.join(words)
    tokenizer.fit_on_texts([headers_clean])
    headers_sequence = tokenizer.texts_to_sequences([headers_clean])
    headers_padded = pad_sequences(headers_sequence, maxlen=50, padding='post')
    return headers_padded

def worldcloud(email_content):
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



def predict_phising(email_content):
    preprocessed_content = preprocess_content(email_content)

    prediction = model.predict(preprocessed_content)
    # confidence = max(model.predict_proba(preprocessed_content))
    confidence = prediction[0][0]
    prediction = prediction[0][0] > 0.5

    return {
        'email_content': email_content,
        'is_phishing': prediction,
        'confidence': confidence
    }

def load_model(path):
    return model

