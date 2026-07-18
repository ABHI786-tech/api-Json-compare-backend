from pydantic import BaseModel
from typing import Dict, Any, Optional
from datetime import datetime


class JSONComparisonBase(BaseModel):
    json1: Dict[str, Any]
    json2: Dict[str, Any]
    comparison_result: Optional[Dict[str, Any]] = None


class JSONComparisonCreate(JSONComparisonBase):
    pass


class JSONComparisonResponse(JSONComparisonBase):
    id: int
    share_token: str
    created_at: datetime

    class Config:
        from_attributes = True
