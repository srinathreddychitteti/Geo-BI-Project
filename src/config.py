# src/config.py
"""
Configuration constants for the Geo-Spatial Business Intelligence Chatbot.
"""

# --- API Endpoints ---
NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"
OVERPASS_URL = "https://overpass.kumi.systems/api/interpreter"

# --- Application Metadata ---
# Used for the User-Agent header in API requests to identify our application.
# It's good practice to provide a way for API administrators to contact you.
APP_USER_AGENT = "GeoChatbot/1.0 (srinath@example.com)" # TODO: Replace with your actual contact email

# --- Overpass API Query Settings ---
# Search radius in meters around the geocoded coordinates.
SEARCH_RADIUS_METERS = 1500
# API timeout in seconds.
API_TIMEOUT_SECONDS = 25