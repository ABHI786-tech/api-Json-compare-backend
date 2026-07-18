from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from config.database import Base
import secrets


class JSONComparison(Base):
    __tablename__ = "json_comparisons"

    id = Column(Integer, primary_key=True, index=True)
    share_token = Column(String, unique=True, index=True, nullable=False, default=lambda: secrets.token_urlsafe(16))
    json1 = Column(String, nullable=False)
    json2 = Column(String, nullable=False)
    comparison_result = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
