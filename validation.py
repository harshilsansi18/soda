from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from backend.database import Base
from datetime import datetime

class Validation(Base):
    __tablename__ = "validations"

    id = Column(Integer, primary_key=True, index=True)
    asset_id = Column(Integer, ForeignKey("assets.id"), nullable=False)
    status = Column(String, nullable=False)  # Passed / Failed
    created_at = Column(DateTime, default=datetime.utcnow)

    asset = relationship("Asset")


class ValidationResult(Base):
    __tablename__ = "validation_results"

    id = Column(Integer, primary_key=True, index=True)
    table_name = Column(String, nullable=False)  # The table validated
    check_name = Column(String, nullable=False)  # Name of the check (e.g., "missing_count(email) = 0")
    check_status = Column(String, nullable=False)  # Passed / Failed
    check_value = Column(String, nullable=True)  # Example: 3 missing values
    timestamp = Column(DateTime(timezone=True), server_default=func.now())  # When validation ran
