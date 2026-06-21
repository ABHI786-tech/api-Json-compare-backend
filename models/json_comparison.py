from sqlalchemy import Column, Integer, String, DateTime, JSON
from sqlalchemy.sql import func
from config.database import Base


class JSONComparison(Base):
    __tablename__ = "json_comparisons"

    id = Column(Integer, primary_key=True, index=True)
    json1 = Column(JSON, nullable=False)
    json2 = Column(JSON, nullable=False)
    comparison_result = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
