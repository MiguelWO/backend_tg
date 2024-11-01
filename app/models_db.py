from sqlalchemy import Boolean, DateTime, Float, create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

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
    predictions = relationship('Prediction', back_populates='model')

# Create an engine that stores data in the local directory's
# sqlalchemy_example.db file.
engine = create_engine('sqlite:///sqlalchemy_example.db')
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) 

# Create all tables in the engine. This is equivalent to "Create Table"
# statements in raw SQL.
Base.metadata.create_all(engine)