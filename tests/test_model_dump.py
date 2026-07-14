
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, JSON
from sqlalchemy.sql import func
from config.database import Base
from schemas.json_comparison import JSONComparisonResponse
from config.utils import encode_id

class TestComp(Base):
    __tablename__ = "test"
    id = Column(Integer, primary_key=True)
    json1 = Column(JSON)
    json2 = Column(JSON)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

test_comp = TestComp()
test_comp.id = 23
test_comp.json1 = {"a":1}
test_comp.json2 = {"a":2}
test_comp.created_at = datetime.now()

response = JSONComparisonResponse.model_validate(test_comp)
print("response:", response)
print("response.id:", response.id, type(response.id))
encoded_response = response.model_dump(mode="json")
print("encoded_response before encode_id:", encoded_response)
print("encoded_response['id'] before encode_id:", encoded_response["id"], type(encoded_response["id"]))
encoded_response["id"] = encode_id(encoded_response["id"])
print("encoded_response after encode_id:", encoded_response)
print("encoded_response['id'] after encode_id:", encoded_response["id"], type(encoded_response["id"]))
