import pytest
import json
from pathlib import Path
from unittest.mock import patch
from even_wear_shuffle.processor import get_all_releases_cleaned

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