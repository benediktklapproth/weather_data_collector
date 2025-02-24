import requests
import pandas as pd
from datetime import datetime
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Mapping of German states with adminCode1
STATE_CODES = {
    "01": "Baden-Württemberg",
    "02": "Bayern",
    "03": "Bremen",
    "04": "Hamburg",
    "05": "Hessen",
    "06": "Niedersachsen",
    "07": "Nordrhein-Westfalen",
    "08": "Rheinland-Pfalz",
    "09": "Saarland",
    "10": "Schleswig-Holstein",
    "11": "Brandenburg",
    "12": "Mecklenburg-Vorpommern",
    "13": "Sachsen",
    "14": "Sachsen-Anhalt",
    "15": "Thüringen",
    "16": "Berlin"
}

def fetch_top_cities(state_code: str = None) -> pd.DataFrame:
    """
    Fetch the top 50 populous cities in a given German state or all states.
    
    Args:
        state_code (str): The admin code of the state. If None, fetch for all states.
    
    Returns:
        pd.DataFrame: DataFrame containing city data.
    """
    base_url = "http://api.geonames.org/searchJSON"
    username = "benediktklapproth"
    params = {
        "country": "DE",
        "featureClass": "P",
        "fcode": ["PPL", "PPLA", "PPLA2", "PPLA3", "PPLC"],
        "maxRows": 50,
        "orderby": "population",
        "username": username
    }

    cities_data = []

    if state_code:
        params["adminCode1"] = state_code
        response = requests.get(base_url, params=params)
        if response.status_code == 200:
            data = response.json()
            cities_data.extend(data.get("geonames", []))
        else:
            logger.error(f"Error fetching data for state {state_code}: {response.status_code}")
    else:
        for code in STATE_CODES:
            params["adminCode1"] = code
            response = requests.get(base_url, params=params)
            if response.status_code == 200:
                data = response.json()
                cities_data.extend(data.get("geonames", []))
            else:
                logger.error(f"Error fetching data for state {code}: {response.status_code}")

    df = pd.DataFrame([{
        "city": city.get("name"),
        "adminCode1": city.get("adminCode1"),
        "region": STATE_CODES.get(city.get("adminCode1")),
        "population": city.get("population"),
        "latitude": city.get("lat"),
        "longitude": city.get("lng")
    } for city in cities_data])

    return df

def fetch_weather_data(lat: float, lon: float) -> dict:
    """
    Fetch weather data for a specific city.
    
    Args:
        lat (float): Latitude of the city.
        lon (float): Longitude of the city.
    
    Returns:
        dict: Dictionary containing weather data. All timestamps are in UTC.
    """
    api_key = "6e51c4a9460b2a46edba90f86ed40ba2"
    base_url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "lat": lat,
        "lon": lon,
        "appid": api_key,
        "units": "metric"
    }

    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        data = response.json()
        weather = {
            "temperature": data["main"]["temp"],
            "feels_like": data["main"]["feels_like"],
            "temp_min": data["main"]["temp_min"],
            "temp_max": data["main"]["temp_max"],
            "pressure": data["main"]["pressure"],
            "humidity": data["main"]["humidity"],
            "sea_level": data["main"].get("sea_level"),
            "grnd_level": data["main"].get("grnd_level"),
            "visibility": data.get("visibility"),
            "wind_speed": data["wind"]["speed"],
            "wind_deg": data["wind"]["deg"],
            "wind_gust": data["wind"].get("gust"),
            "rain_1h": data.get("rain", {}).get("1h"),
            "clouds_all": data["clouds"]["all"],
            "weather_description": data["weather"][0]["description"],
            "timestamp": datetime.utcfromtimestamp(data["dt"]).isoformat()
        }
        return weather
    else:
        logger.error(f"Error when fetching weather data for coordinates ({lat}, {lon}): {response.status_code}")
        return None