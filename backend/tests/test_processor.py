import pytest
import json
from pathlib import Path
from unittest.mock import patch
from even_wear_shuffle.processor import get_all_releases_cleaned, clean_release_data

def load_fixture(filename):
    """Helper to load real JSON data for our mocks."""
    path = Path(__file__).parent / "fixtures" / filename
    with open(path, 'r') as f:
        return json.load(f)

@patch("even_wear_shuffle.processor.test_connection")
def test_get_all_releases_cleaned(mock_test_connection):
    # Setup the mock to return our predefined responses
    mock_test_connection.side_effect = [load_fixture("discogs_response_page_1_50perpage_full.json"), 
                                        load_fixture("discogs_response_page_2_50perpage_full.json"),
                                        load_fixture("discogs_response_page_3_50perpage_only3releases.json")]

    params = {"per_page": 50, "page": 1}
    result = get_all_releases_cleaned(params)
    
    # Assertions to check if the function is working as expected with first and last item in test data
    assert result[0]["artist"] == "Maroon 5"
    assert result[0]["album"] == "V"
    assert result[0]["id"] == 6102844
    assert result[0]["played"] == 0
    assert result[0]["skipped"] == 0
    assert result[0]["link"] == "https://www.discogs.com/release/6102844"
    assert result[-1]["artist"] == "Adele (3)"
    assert result[-1]["album"] == "25"
    assert result[-1]["id"] == 7714672
    assert result[-1]["played"] == 0
    assert result[-1]["skipped"] == 0
    assert result[-1]["link"] == "https://www.discogs.com/release/7714672"
    assert len(result) == 103  # 50 from page 1, 50 from page 2, and 3 from page 3
    
    # Verify the API was called exactly three times
    assert mock_test_connection.call_count == 3
    
def test_clean_release_data_malformed_response():
    # This file contains 10 releases with various malformed edge cases to test robustness
    raw_data = load_fixture("malformed_releases.json")
    
    # Run the parser since this is the core logic where edge cases should be handled
    result = clean_release_data(raw_data.get("releases", []))
    
    # Case 0: missing id field entirely
    assert result[0]["id"] is None
    assert "None" in result[0]["link"]  
    
    # Case 1: missing name field in artists
    assert result[1]["artist"] == "Unknown"
    
    # Case 2: missing title field entirely
    assert result[2]["album"] == "Unknown"
    
    # Case 3: missing entire basic information key
    assert result[3]["artist"] == "Unknown"
    assert result[3]["album"] == "Unknown"

    # Case 4: missing entire basic information content ({})
    assert result[4]["artist"] == "Unknown"
    assert result[4]["album"] == "Unknown"
    
    # Case 5: setting basic_information to null
    assert result[5]["artist"] == "Unknown"
    assert result[5]["album"] == "Unknown"
    
    # Case 6: missing artists content entirely (empty list [])
    assert result[6]["artist"] == "Unknown"
    
    # Case 7: multiple artists
    assert result[7]["artist"] is not None 
    assert result[7]["artist"] != "Unknown"
    
    # Case 8: Empty title ("")
    assert result[8]["album"] == ""
    
    # Case 9: id as a string instead of an int ("12345")
    assert isinstance(result[9]["id"], str)