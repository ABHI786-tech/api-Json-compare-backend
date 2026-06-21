from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from config.database import get_db
from models import JSONComparison
from schemas import JSONComparisonCreate, JSONComparisonResponse

router = APIRouter(tags=["JSON Comparisons"])


@router.post("/josn", response_model=JSONComparisonResponse)
def create_json_comparison(comparison: JSONComparisonCreate, db: Session = Depends(get_db)):
    db_comparison = JSONComparison(
        json1=comparison.json1,
        json2=comparison.json2,
        comparison_result=comparison.comparison_result
    )
    db.add(db_comparison)
    db.commit()
    db.refresh(db_comparison)
    return db_comparison


@router.get("/json", response_model=List[JSONComparisonResponse])
def get_all_json_comparisons(db: Session = Depends(get_db)):
    comparisons = db.query(JSONComparison).all()
    return comparisons


@router.get("/json/{comparison_id}", response_model=JSONComparisonResponse)
def get_json_comparison(comparison_id: int, db: Session = Depends(get_db)):
    comparison = db.query(JSONComparison).filter(JSONComparison.id == comparison_id).first()
    if comparison is None:
        raise HTTPException(status_code=404, detail="Comparison not found")
    return comparison
