# Xtream Codes IPTV Data Extractor

This Python script extracts live streams, VOD streams, and series data from Xtream Codes IPTV providers and saves the information to CSV files.

## Features

*   **Multiple Provider Support:** Reads provider details (URL, username, password) from a YAML configuration file.
*   **Data Extraction:** Retrieves live streams, VOD streams, and series, including their associated categories.
*   **CSV Output:** Saves extracted data to separate CSV files for each provider and stream type (live, VOD, series).
*   **Timestamped Filenames:** Appends a UTC timestamp to each CSV filename to ensure uniqueness (e.g., `ProviderName_live_streams_20231027_153000.csv`).
*   **Error Handling:** Includes error handling for API request failures, JSON parsing errors, and missing data.
*   **Logging:** Logs script progress, warnings, and errors to the console.

## Requirements

*   Python 3.6+
*   `requests` library (>= 2.31.0 recommended)
*   `PyYAML` library (>= 6.0.1 recommended)

You can install the required libraries using `pip`:

```bash
pip install -r requirements.txt
```

## Configuration

`providers.yaml`: Create a YAML file named `providers.yaml` in the same directory as the script. This file will contain the details for your Xtream Codes providers.

Example `providers.yaml`:

```yaml
---
providers:
  - name: ProviderOne
    url: "http://providerone.com:8000"  # Replace with your provider's URL
    username: "your_username"  # Replace with your username
    password: "your_password"  # Replace with your password
  - name: ProviderTwo
    url: "http://providertwo.tv:8080"
    username: "your_username"
    password: "your_password"
  # Add more providers as needed...
```

Placeholders: Replace the placeholder values in `providers.yaml` with your actual provider URLs, usernames, and passwords.

## Usage
1. Clone the repository or download the Python script and save it as a .py file (e.g., xtream_extractor.py).

2. Install the required libraries:
```bash
pip install -r requirements.txt
```

3. Create and configure `providers.yaml` as described above.

4. Run the script:
```bash
python xtream_to_csv.py
```

## Output
The script will generate CSV files in the same directory where it is executed. The filenames will follow this pattern:

```
{provider_name}_live_streams_{timestamp}.csv
{provider_name}_vod_streams_{timestamp}.csv
{provider_name}_series_streams_{timestamp}.csv
```

Where:
    `{provider_name}` is the name of the provider as specified in xtream_providers.yaml.
    `{timestamp}` is the UTC date and time when the script was executed in the format YYYYmmddTHHMMSSZ.

Example CSV Output (Live Streams):
```csv
category_name	name	num	stream_icon	epg_channel_id	is_adult	...other fields...
Movies	Movie 1	1	http://example.com/icons/movie1.png			...
Sports	Sports 2	2	http://example.com/icons/sports2.png	sports_channel		...
News	News 1	3	http://example.com/icons/news1.png	news_channel		...
```

## Notes

- API Endpoints: The script uses common Xtream Codes API endpoints. However, the availability and exact behavior of these endpoints might vary slightly depending on the Xtream Codes version and server configuration.
- Error Handling: The script includes basic error handling, but it's always a good practice to monitor the console output for any warnings or errors.
- Ethical Use: Please use this script responsibly and ethically. Only use it to access data from providers for which you have legitimate access. Respect the terms of service of your IPTV providers.
- Column Order: You can customize the column order for each stream type in the save_streams_to_csv() function by modifying the ordered_fieldnames list.

## Troubleshooting

`Error: No live streams found for ...`: This error might indicate that the API request failed or that the provider doesn't have any live streams. Check the provider URL, username, and password in xtream_providers.yaml.

`Error parsing JSON response...`: This error could indicate an issue with the API response format. Check the Xtream Codes version and server configuration.

`Error during API request...`: This error usually indicates a network issue or a problem with the API server. Make sure your internet connection is working and that the provider's API server is online.

If you encounter any other issues, please open an issue.