import argparse
import os
from data_loader import fetch_top_cities, fetch_weather_data
import pandas as pd
from datetime import datetime
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    # Define CLI arguments
    parser = argparse.ArgumentParser(description="Fetch the top 50 populous cities in a given German state and their weather data.")
    parser.add_argument("--state", type=str, help="State admin code (e.g., '13' for Sachsen). If not provided, data for all states will be fetched.")
    parser.add_argument("--output", type=str, required=True, help="Directory where the output CSV files will be saved.")
    parser.add_argument("--exclude", type=str, nargs='*', help="Weather parameters to exclude (e.g., temperature humidity weather_description).")

    args = parser.parse_args()

    # 1. Fetch city data
    logger.info("Fetching city data...")
    cities_df = fetch_top_cities(state_code=args.state)

    if cities_df.empty:
        logger.error("No data fetched. Check your input or API connection.")
        return

    # 2. Fetch weather data
    logger.info("Fetching weather data...")
    weather_data = []
    for _, row in cities_df.iterrows():
        weather = fetch_weather_data(row['latitude'], row['longitude'])
        if weather:
            weather['city'] = row['city']
            weather_data.append(weather)
        else:
            logger.error(f"Failed to fetch weather data for city: {row['city']}")

    weather_df = pd.DataFrame(weather_data)

    # 3. Exclude columns if specified
    if args.exclude:
        weather_df.drop(columns=args.exclude, inplace=True)

    # 4. Aggregate city and weather data to a single DataFrame
    result_df = pd.merge(cities_df, weather_df, on='city')

    # 5. Save data to output directory as CSV
    output_dir = os.path.abspath(args.output)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    state_code = args.state if args.state else "00"
    current_time = datetime.now().strftime("%Y-%m-%d_%H")
    output_path = os.path.join(output_dir, f"weather_data_{state_code}_{current_time}.csv")

    if os.path.exists(output_path):
        logger.warning(f"Data for {current_time} already exists. Skipping fetch.")
    else:
        result_df.to_csv(output_path, index=False)
        logger.info(f"Data successfully saved to {output_path}")

# Execute the script when called directly from the CLI
if __name__ == "__main__":
    main()