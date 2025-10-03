import pytest
from unittest.mock import MagicMock
from src.locationFetcher import geocode_location, get_business_data

# Test geocode_location function
def test_geocode_location_success(mocker):
    """Test successful geocoding."""
    mock_response = MagicMock()
    mock_response.json.return_value = [{"lat": "17.41", "lon": "78.43"}]
    mocker.patch("requests.get", return_value=mock_response)
    
    result = geocode_location("Banjara Hills")
    assert result == {"lat": "17.41", "lon": "78.43"}

def test_geocode_location_no_results(mocker):
    """Test geocoding with no results found."""
    mock_response = MagicMock()
    mock_response.json.return_value = []
    mocker.patch("requests.get", return_value=mock_response)
    
    result = geocode_location("NonExistentPlace")
    assert result is None

# Test get_business_data function
def test_get_business_data_success(mocker):
    """Test successful fetching of business data."""
    mocker.patch("src.location_fetcher.geocode_location", return_value={"lat": "17.41", "lon": "78.43"})
    
    mock_overpass_response = MagicMock()
    mock_overpass_response.json.return_value = {
        "elements": [
            {"tags": {"name": "Cafe Coffee Day", "amenity": "cafe"}},
            {"tags": {"name": "Starbucks", "shop": "coffee"}},
            {"tags": {}} # Element with no name tag
        ]
    }
    mocker.patch("requests.post", return_value=mock_overpass_response)
    
    result = get_business_data("Banjara Hills", "cafe")
    assert isinstance(result, list)
    assert len(result) == 2
    assert result[0]["name"] == "Cafe Coffee Day"
    assert result[1]["name"] == "Starbucks"

def test_get_business_data_no_coords(mocker):
    """Test behavior when geocoding fails."""
    mocker.patch("src.location_fetcher.geocode_location", return_value=None)
    
    result = get_business_data("InvalidPlace", "restaurant")
    assert "Error: Could not find coordinates" in result