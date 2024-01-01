# models.py

from datetime import datetime

from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column(String(8), primary_key=True)
    name = Column(String(255), nullable=False)
    score = Column(Integer, default=0)
    unlock_id = Column(String(255), default="")
    modified_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
