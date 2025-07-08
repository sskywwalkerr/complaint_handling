from sqlalchemy import Column, Integer, String, DateTime, Float, JSON
from datetime import datetime



from app.db import Base


class Complaint(Base):
    __tablename__ = "complaints"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    text = Column(String(500), nullable=False)
    status = Column(String(20), default="open")
    timestamp = Column(DateTime, default=datetime.utcnow)
    sentiment = Column(String(20), default="unknown")
    category = Column(String(50), default="другое")
    location = Column(JSON, nullable=True)