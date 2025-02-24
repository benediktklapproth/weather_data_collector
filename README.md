# Weather Data Collector

A Python tool for dynamically collecting weather data and generating hourly time series for the 50 most populous cities in a selected region. It uses Geonames and OpenWeatherMap APIs, supports customizable data exclusions, and stores results in CSV format for efficient processing in Databricks.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Parameters](#parameters)
- [Examples](#examples)

## Installation

1. **Clone the repository:**

    ```sh
    git clone https://github.com/yourusername/weather_data_collector.git
    cd weather_data_collector
    ```

2. **Create a virtual environment:**

    ```sh
    python -m venv .venv
    ```

3. **Activate the virtual environment:**

    - On Windows:

        ```sh
        .venv\Scripts\activate
        ```

    - On macOS/Linux:

        ```sh
        source .venv/bin/activate
        ```

4. **Install the required packages:**

    ```sh
    pip install -r requirements.txt
    ```

## Usage

To run the script, use the following command:

```sh
python src/main.py --state <state_code> --output <output_directory> [--exclude <weather_parameters>]
```

**Note:** All timestamps in the output CSV files are in UTC.

## Parameters

- `--state <state_code>`: The state admin code for which to collect weather data (e.g., '13' for Sachsen). If not provided, data for all states will be fetched.
  - Available state codes:
    - `01`: Baden-Württemberg
    - `02`: Bayern
    - `03`: Bremen
    - `04`: Hamburg
    - `05`: Hessen
    - `06`: Niedersachsen
    - `07`: Nordrhein-Westfalen
    - `08`: Rheinland-Pfalz
    - `09`: Saarland
    - `10`: Schleswig-Holstein
    - `11`: Brandenburg
    - `12`: Mecklenburg-Vorpommern
    - `13`: Sachsen
    - `14`: Sachsen-Anhalt
    - `15`: Thüringen
    - `16`: Berlin
- `--output <output_directory>`: The directory where the output CSV files will be saved.
- `--exclude <weather_parameters>`: (Optional) A space-separated list of weather parameters to exclude from the data collection. Possible values include `temperature`, `humidity`, `pressure`, etc.

## Examples

1. **Collect weather data for Sachsen and save to the specified output directory:**

    ```sh
    python src/main.py --state 13 --output ./data
    ```

2. **Collect weather data for all states, excluding temperature and humidity:**

    ```sh
    python src/main.py --output ./data --exclude temperature humidity
    ```