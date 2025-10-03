import requests
import json
import logging
from typing import Dict, List, Optional, Any, Union

# Local application imports
import config

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def geocode_location(query: str) -> Optional[Dict[str, str]]:
    """
    Converts a location name into latitude and longitude using OSM Nominatim.

    Args:
        query: The location name to geocode (e.g., "Banjara Hills, Hyderabad").

    Returns:
        A dictionary containing 'lat' and 'lon' if successful, otherwise None.
    """
    params = {'q': query, 'format': 'json', 'limit': 1}
    headers = {'User-Agent': config.APP_USER_AGENT}
    
    try:
        response = requests.get(config.NOMINATIM_URL, params=params, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        if data:
            logging.info(f"Successfully geocoded '{query}'.")
            return {"lat": data[0]["lat"], "lon": data[0]["lon"]}
        logging.warning(f"No geocoding results found for '{query}'.")
        return None
    except requests.exceptions.RequestException as e:
        logging.error(f"Geocoding request failed for '{query}': {e}")
        return None
    except (json.JSONDecodeError, IndexError) as e:
        logging.error(f"Failed to parse geocoding response for '{query}': {e}")
        return None

def get_business_data(query: str, business_type: str) -> Union[List[Dict[str, Any]], str]:
    """
    Fetches business data from OpenStreetMap's Overpass API.

    Args:
        query: The location name (e.g., "Ameerpet, Hyderabad").
        business_type: The type of business to search for (e.g., "cafe").

    Returns:
        A list of dictionaries, each representing a business, or an error string
        if the operation fails.
    """
    coords = geocode_location(query)
    if not coords:
        return f"Error: Could not find coordinates for '{query}'. Please try a more specific location."

    # A more robust Overpass query searching common OSM tags.
    overpass_query = f"""
    [out:json][timeout:{config.API_TIMEOUT_SECONDS}];
    (
      node[~"^(amenity|shop|craft)$"~"{business_type}",i](around:{config.SEARCH_RADIUS_METERS},{coords['lat']},{coords['lon']});
      way[~"^(amenity|shop|craft)$"~"{business_type}",i](around:{config.SEARCH_RADIUS_METERS},{coords['lat']},{coords['lon']});
      relation[~"^(amenity|shop|craft)$"~"{business_type}",i](around:{config.SEARCH_RADIUS_METERS},{coords['lat']},{coords['lon']});
    );
    out center;
    """

    try:
        response = requests.post(config.OVERPASS_URL, data={'data': overpass_query}, timeout=config.API_TIMEOUT_SECONDS)
        response.raise_for_status()
        data = response.json()
        logging.info(f"Successfully fetched data for '{business_type}' in '{query}'.")

        business_list = []
        for element in data.get('elements', []):
            tags = element.get('tags', {})
            name = tags.get('name')
            # Only include businesses that have a name.
            if name:
                business_list.append({
                    "name": name,
                    "type": tags.get('amenity') or tags.get('shop') or tags.get('craft') or 'unknown'
                })
        return business_list

    except requests.exceptions.RequestException as e:
        logging.error(f"Overpass API request failed: {e}")
        return "Error: Failed to fetch data from OpenStreetMap's API due to a network issue."
    except json.JSONDecodeError:
        logging.error("Failed to parse JSON response from Overpass API.")
        return "Error: Failed to parse the response from OpenStreetMap's API."