"""
This script is responsible for exporting the cleaned release data into a CSV to test what could be used 
as the backend hosted by Google Sheets later. It relies on the processor module to get the cleaned data.
"""

__author__ = "Omar Ramos Escoto"

import csv
from pathlib import Path
from typing import Any, Dict


from even_wear_shuffle.processor import get_all_releases_cleaned
from even_wear_shuffle.discogs_api_check import test_connection


def export_to_csv(releases: list[Dict[str, Any]], output_filename: str = "discogs_collection.csv") -> None:
    """
    Exports the cleaned release data into a CSV that will be used as the backend hosted by Google Sheets later
    """

    fieldnames = releases[0].keys()

    # Using DictWriter since the data is already in dict format
    with open(output_filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerows(releases)

    print(f"All {len(releases)} releases writen to {output_filename}")


if __name__ == "__main__":
    params = {"per_page": 50, "page": 1}
    all_releases = get_all_releases_cleaned(params)

    output_file = Path(__file__).resolve().parent.parent / "test_data" / "testing_csv_exporter.csv"

    export_to_csv(all_releases, output_file)
