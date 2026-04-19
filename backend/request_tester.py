import requests
import json

payload = {
  "time": "",
  "team_size": "",
  "budget": "",
  "roadmap": []
}

try:
    res = requests.post("http://localhost:8000/api/run/stakeholder", json=payload)
    print(res.status_code)
    print(res.text)
except Exception as e:
    print(e)
