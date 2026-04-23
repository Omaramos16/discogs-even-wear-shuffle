"""
Processor module for transforming raw Discogs API data into a readable format.
"""

__author__ = "Omar Ramos Escoto"

import os
import json
from dotenv import load_dotenv
from typing import List, Dict, Any

from scripts.tests.discogs_api_check import test_connection


def clean_release_data(raw_releases: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Transforms nested Discogs API items into flat list.
    """
    
    return [
        {
            "id": r.get("id"),
            "artist": r.get("basic_information", {}).get("artists", [{}])[0].get("name", "Unknown"),
            "album": r.get("basic_information", {}).get("title", "Unknown"),
            "played": 0,
            "skipped": 0,
            "link": f"https://www.discogs.com/release/{r.get('id')}"
        }
        for r in raw_releases.get("releases", [])
    ]
    

if __name__ == "__main__":
    output = test_connection()
    if output:
        print("Got data back from discogs, now processing it:")
        cleaned_data = clean_release_data(output)
        print(json.dumps(cleaned_data, indent = 4))
    else:
        print("No data received from discogs, check your connection and credentials.")
              