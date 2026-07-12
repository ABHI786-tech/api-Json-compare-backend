from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from config.cache import (
    ALL_COMPARISONS_KEY,
    cache_get,
    cache_set,
    comparison_key,
    invalidate_list_cache,
)
from config.database import get_db
from models import JSONComparison
from schemas import JSONComparisonCreate, JSONComparisonResponse

router = APIRouter(tags=["JSON Comparisons"])


@router.post("/json", response_model=JSONComparisonResponse)
def create_json_comparison(comparison: JSONComparisonCreate, db: Session = Depends(get_db)):
    db_comparison = JSONComparison(
        json1=comparison.json1,
        json2=comparison.json2,
        comparison_result=comparison.comparison_result,
    )
    db.add(db_comparison)
    db.commit()
    db.refresh(db_comparison)

    response = JSONComparisonResponse.model_validate(db_comparison)
    cache_set(comparison_key(db_comparison.id), response.model_dump(mode="json"))
    invalidate_list_cache()

    return response


@router.get("/json", response_model=List[JSONComparisonResponse])
def get_all_json_comparisons(db: Session = Depends(get_db)):
    cached = cache_get(ALL_COMPARISONS_KEY)
    if cached is not None:
        return [JSONComparisonResponse.model_validate(item) for item in cached]

    comparisons = db.query(JSONComparison).all()
    response = [JSONComparisonResponse.model_validate(item) for item in comparisons]
    cache_set(ALL_COMPARISONS_KEY, [item.model_dump(mode="json") for item in response])
    return response


@router.get("/json/{comparison_id}", response_model=JSONComparisonResponse)
def get_json_comparison(comparison_id: int, db: Session = Depends(get_db)):
    cached = cache_get(comparison_key(comparison_id))
    if cached is not None:
        return JSONComparisonResponse.model_validate(cached)

    comparison = db.query(JSONComparison).filter(JSONComparison.id == comparison_id).first()
    if comparison is None:
        raise HTTPException(status_code=404, detail="Comparison not found")

    response = JSONComparisonResponse.model_validate(comparison)
    cache_set(comparison_key(comparison_id), response.model_dump(mode="json"))
    return response


@router.put("/json/{comparison_id}", response_model=JSONComparisonResponse)
def update_json_comparison(
    comparison_id: int,
    comparison: JSONComparisonCreate,
    db: Session = Depends(get_db),
):
    db_comparison = db.query(JSONComparison).filter(JSONComparison.id == comparison_id).first()
    if db_comparison is None:
        raise HTTPException(status_code=404, detail="Comparison not found")

    db_comparison.json1 = comparison.json1
    db_comparison.json2 = comparison.json2
    db_comparison.comparison_result = comparison.comparison_result
    db.commit()
    db.refresh(db_comparison)

    response = JSONComparisonResponse.model_validate(db_comparison)
    cache_set(comparison_key(comparison_id), response.model_dump(mode="json"))
    invalidate_list_cache()

    return response
