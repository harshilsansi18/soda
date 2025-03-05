from sqlalchemy import Column, Integer, String, DateTime
from backend.database import Base
from datetime import datetime

class Asset(Base):
    __tablename__ = "assets"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    type = Column(String, nullable=False)  # Example: CSV, JSON, etc.
    created_at = Column(DateTime, default=datetime.utcnow)
