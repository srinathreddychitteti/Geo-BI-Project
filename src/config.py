# src/config.py
"""
Configuration constants for the Geo-Spatial Business Intelligence Chatbot.
"""

# --- API Endpoints ---
NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"
OVERPASS_URL = "https://overpass.kumi.systems/api/interpreter"

# --- Application Metadata ---
APP_USER_AGENT = "GeoChatbot/1.0 (srinathreddychitteti@gmail.com)" 

# --- Overpass API Query Settings ---
# Search radius in meters around the geocoded coordinates.
SEARCH_RADIUS_METERS = 1500

API_TIMEOUT_SECONDS = 25