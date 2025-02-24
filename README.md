# Weather Data Collector

A Python tool for dynamically collecting weather data and generating hourly time series for the 50 most populous cities in a selected region. It uses Geonames and OpenWeatherMap APIs, supports customizable data exclusions, and stores results in CSV format for efficient processing in Databricks.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Parameters](#parameters)
- [Examples](#examples)
- [API Documentations](#api-documentation)
- [Approach and Development Process](#-approach-and-development-process)

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

- `--state <state_code>`: (Optional) The state admin code for which to collect weather data (e.g., '13' for Sachsen). If not provided, data for all states will be fetched.
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
- `--output <output_directory>`: (Required) The directory where the output CSV files will be saved.
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

## API Documentation
- https://www.geonames.org/
    https://www.geonames.org/export/ws-overview.html
    https://www.geonames.org/export/codes.html
- https://openweathermap.org/api
    https://openweathermap.org/current
    https://openweathermap.org/history
    https://openweathermap.org/bulk


## 🔍 Approach and Development Process
At the beginning of this project, I carefully considered the most suitable architecture to ensure both modularity and scalability without overcomplicating the structure for the relatively small scope of the task. I decided on a modular structure, as it offered the best balance between scalability, maintainability, and complexity.

Initially, I planned to store the data in Parquet format due to its excellent compatibility with Databricks and efficient compression capabilities. However, setting up Hadoop to handle Parquet files without additional packages beyond PySpark proved to be overly complex. This setup required defining various environment variables, raising concerns about whether it would integrate seamlessly with the target system. As a result, I shifted to using CSV files for simplicity and broader compatibility.

Next, I explored the APIs and their documentation, which were well-structured and easy to follow. For simplicity and transparency, I chose not to store the API key in an environment variable, since it uses a free license with a limited number of requests and poses no security or cost risk.

For the weather data, my optimal solution would have involved passing a start date as a parameter and fetching all missing hourly data from that point onward. I had already written a script that looped through each hour from the start date to the current time and generated individual daily CSV files with historical weather data for each city. However, since OpenWeatherMap's historical data service is only available to paid or verified student accounts, I was unable to implement this solution fully before the deadline due to pending verification of my student account.

As a result, the current implementation only supports fetching current weather data. A significant limitation of this approach is that any data gaps caused by failed executions cannot be automatically filled afterward. An alternative would have been using the Historic Bulk API, which provides hourly historical data for the past seven days, but this service also requires a paid subscription and may not cover all required cities and coordinates (fixed 210k cities).

In the following steps, I progressively loaded the data, ensuring the format was correct and gradually expanded the functionality until it met the project requirements. I also implemented error handling and tested the functionality thoroughly. Once the logic was complete, I refined the code style, added comments and docstrings for better readability, and removed redundant code from earlier development attempts.

Finally, I prepared the project for deployment by creating a comprehensive README.md and a requirements.txt file to ensure easy installation and execution.
