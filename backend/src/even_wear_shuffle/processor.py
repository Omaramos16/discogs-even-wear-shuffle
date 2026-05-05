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

    cleaned_data: List[Dict[str, Any]] = []
    for release in raw_releases:
        if release is not None and isinstance(release, dict):
            cleaned_item = {}

            # Set defaults and fetch key values with error handling
            song_id = release.get("id", 0)
            basic_info = release.get("basic_information", {}) or {}  # Handle case where basic_information is None
            artist_name = "Unknown"
            album_title = "Unknown"

            # Most of the information is in the basic_information key
            if basic_info:
                album_title = basic_info.get("title", "Unknown")

                if song_id == 0:  # If id is missing at the top level, try to get it from basic_information
                    song_id = basic_info.get("id", 0)

                artists = basic_info.get("artists", [])
                if isinstance(artists, list) and artists:
                    artist_name = artists[0].get("name", "Unknown")  # List under the first artist
                else:
                    artist_name = "Unknown"

            cleaned_item = {
                "id": song_id,
                "artist": artist_name,
                "album": album_title,
                "played": 0,
                "skipped": 0,
                "link": f"https://www.discogs.com/release/{song_id}"
            }
            cleaned_data.append(cleaned_item)

    return cleaned_data


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
