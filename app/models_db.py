from sqlalchemy import Boolean, DateTime, Float, create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker, Session
import os

Base = declarative_base()

class Prediction(Base):
    __tablename__ = 'predictions'

    id = Column(Integer, primary_key=True)
    email_content = Column(String)
    prediction = Column(Boolean)
    confidence = Column(Float)
    model_id = Column(Integer, ForeignKey('models.id'))
    created_at = Column(DateTime, default = 'CURRENT_TIMESTAMP')

    model = relationship('Model', back_populates='predictions')

class Model(Base):
    __tablename__ = 'models'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    extension = Column(String)
    display_name = Column(String)
    predictions = relationship('Prediction', back_populates='model')


DATABASE_URL = os.getenv('DATABASE_URL')

# Create an engine that stores data in the local directory's
# sqlalchemy_example.db file.
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) 

# Create all tables in the engine. This is equivalent to "Create Table"
# statements in raw SQL.
Base.metadata.create_all(engine)

def initialize_models(db: Session):
    """
    Initialize the models table with available models.
    """
    existing_models = db.query(Model).all()
    if not existing_models:
        db.add_all([
            Model(name='gru_transfer_model', extension='keras', display_name='GRU Transfer Model'),
            Model(name='cnn_lstm_transfer_model', extension='keras', display_name='LSTM Transfer Model'),
            Model(name='phishing_model_keras', extension='keras', display_name='LSTM Model'),
            Model(name='attention_transfer_model', extension='keras', display_name='Attention Transfer Model'),
            Model(name='bilstm_transfer_model', extension='keras', display_name='BiLSTM Transfer Model'),
            Model(name='rnn_transfer_model', extension='keras', display_name='RNN Transfer Model'),
        ])
        db.commit()
    return db.query(Model).all()