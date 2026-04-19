import os
import sys
import pprint
import requests
from dotenv import load_dotenv

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from utils.crustdata_client import get_crustdata_headers

load_dotenv()

url = "https://api.crustdata.com/person/search"
payload = {
    "filters": {
        "op": "and",
        "conditions": [
            {
                "field": "experience.employment_details.current.title",
                "type": "in",
                "value": ["Partner", "Investor", "VC"]
            },
            {
                "field": "basic_profile.headline",
                "type": "contains",
                "value": ["AI", "Tech"]
            }
        ]
    }
}

res = requests.post(url, headers=get_crustdata_headers(), json=payload)
print(res.status_code)
try:
    pprint.pprint(res.json())
except:
    print(res.text)
