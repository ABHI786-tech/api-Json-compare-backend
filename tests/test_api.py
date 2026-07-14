
import requests
import json

url = "http://localhost:8000/json"
data = {"json1": {"a": 1}, "json2": {"a": 2}, "comparison_result": None}

try:
    response = requests.post(url, json=data)
    print("Status Code:", response.status_code)
    print("Raw Response:", response.text)
    print("Response JSON:", json.dumps(response.json(), indent=2))
    print("Type of id in JSON:", type(response.json()["id"]))
except Exception as e:
    print("Error:", str(e))
