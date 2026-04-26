import os
import requests
import json
from dotenv import load_dotenv
from typing import List, Dict, Any

# Load variables from .env
load_dotenv()

TOKEN = os.getenv("DISCOGS_TOKEN")
USERNAME = os.getenv("DISCOGS_USERNAME")


def test_connection(params: Dict[str, Any] = {}) -> Dict[str, Any]:
    url = f"https://api.discogs.com/users/{USERNAME}/collection/folders/0/releases"
    headers = {"Authorization": f"Discogs token={TOKEN}"}

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        print("Success! Connected to Discogs.")
        data = response.json()
        # print(json.dumps(data, indent=4))
        print(f"Total Albums found in page {data['pagination'].get('page', 'N/A')}: {len(data.get('releases', []))}")
        return data
    else:
        print(f"Failed: {response.status_code}")
        print(response.text)
        return {}


if __name__ == "__main__":
    test_connection()
