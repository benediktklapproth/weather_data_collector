import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from data_loader import fetch_top_cities, fetch_weather_data

def test_fetch_top_cities():
    # Test fetching top cities for a specific state (e.g., Sachsen)
    print("Testing fetch_top_cities for state '13' (Sachsen):")
    cities_df = fetch_top_cities(state_code="13")
    print(cities_df.head())

    # Test fetching top cities for all states
    print("\nTesting fetch_top_cities for all states:")
    all_cities_df = fetch_top_cities()
    print(all_cities_df.head())

def test_fetch_weather_data():
    # Test fetching weather data for a specific city (e.g., coordinates for Dresden)
    print("\nTesting fetch_weather_data for coordinates (51.0504, 13.7373) (Dresden):")
    weather_data = fetch_weather_data(lat=51.0504, lon=13.7373)
    print(weather_data)

if __name__ == "__main__":
    test_fetch_top_cities()
    test_fetch_weather_data()