"""
Processor module for transforming raw Discogs API data into a readable format.
"""

__author__ = "Omar Ramos Escoto"

import os
import json
from dotenv import load_dotenv
from typing import List, Dict, Any

from even_wear_shuffle.discogs_api_check import test_connection


def clean_release_data(raw_releases: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Transforms nested Discogs API items into flat list.
    """

    return [
        {
            "id": r.get("id", 0),
            "artist": r.get("basic_information", {}).get("artists", [{}])[0].get("name", "Unknown"),
            "album": r.get("basic_information", {}).get("title", "Unknown"),
            "played": 0,
            "skipped": 0,
            "link": f"https://www.discogs.com/release/{r.get('id')}"
        }
        for r in raw_releases
    ]


def get_all_releases_cleaned(params: Dict[str, int]) -> List[Dict[str, Any]]:
    first_page = test_connection(params)
    if first_page:
        # Extract the releases list and the total number of pages in this collection
        all_releases = clean_release_data(first_page.get("releases", []))
        total_pages = first_page.get("pagination", {}).get("pages", 1)

        for page in range(2, total_pages + 1):
            print(f"Processing page {page} of {total_pages}...")
            params["page"] = page
            page_data = test_connection(params)
            if page_data:
                releases_in_page = clean_release_data(page_data.get("releases", []))
                all_releases.extend(releases_in_page)

    return all_releases


if __name__ == "__main__":
    params = {"per_page": 50, "page": 1}
    all_releases = get_all_releases_cleaned(params)
    print(f"Total cleaned releases: {len(all_releases)}")
    print(json.dumps(all_releases, indent=4))
