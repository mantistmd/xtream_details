import requests
import logging
import csv
import yaml
from datetime import datetime, timezone

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class XtreamCodesAPI:
    # ... (The XtreamCodesAPI class code from the previous responses goes here) ...
    def __init__(self, api_base_url, username, password):
        self.api_base_url = api_base_url
        self.username = username
        self.password = password
        self.base_url = f"{self.api_base_url}/player_api.php"

    def _make_request(self, action, params=None):
        """
        Helper function to make API requests.
        """
        if params is None:
            params = {}
        params['username'] = self.username
        params['password'] = self.password
        params['action'] = action
        url = f"{self.base_url}"

        try:
            response = requests.get(url, params=params)
            response.raise_for_status()  # Raise HTTPError for bad responses
            return response.json()
        except requests.exceptions.RequestException as e:
            logging.error(f"Error during API request: {e}")
            return None
        except ValueError as e:
            logging.error(f"Error parsing JSON response: {e}")
            return None

    def get_user_info(self):
        """
        Get user info and server info.
        """
        return self._make_request("get_user_info")

    def get_live_streams(self):
        """
        Get all live streams.
        """
        return self._make_request("get_live_streams")

    def get_vod_streams(self):
        """
        Get all VOD streams.
        """
        return self._make_request("get_vod_streams")

    def get_series(self):
        """
        Get all series.
        """
        return self._make_request("get_series")

    def get_live_categories(self):
        """
        Get all live categories.
        """
        return self._make_request("get_live_categories")

    def get_vod_categories(self):
        """
        Get all VOD categories.
        """
        return self._make_request("get_vod_categories")

    def get_series_categories(self):
        """
        Get all series categories.
        """
        return self._make_request("get_series_categories")

    def get_vod_info(self, vod_id):
        """
        Get information about a specific VOD stream.
        """
        return self._make_request("get_vod_info", {"vod_id": vod_id})

    def get_series_info(self, series_id):
        """
        Get information about a specific series.
        """
        return self._make_request("get_series_info", {"series_id": series_id})

    def get_epg(self, stream_id, limit=None):
        """
        Get EPG information for a live stream.
        """
        params = {"stream_id": stream_id}
        if limit:
            params["limit"] = limit
        return self._make_request("get_epg", params)

    def get_short_epg(self, stream_id, limit=None):
        """
        Get short EPG information for a live stream.
        """
        params = {"stream_id": stream_id}
        if limit:
            params["limit"] = limit
        return self._make_request("get_short_epg", params)

    def get_m3u_playlist(self, playlist_type="m3u_plus", output_format="ts"):
        """
        Retrieve the M3U playlist URL.

        Args:
            playlist_type: The type of playlist (e.g., "m3u_plus").
            output_format: The desired output format (e.g., "ts", "m3u8").

        Returns:
            The M3U playlist URL as a string, or None if an error occurs.
        """
        url = f"{self.api_base_url}/playlist.php?username={self.username}&password={self.password}&type={playlist_type}&output={output_format}"
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise HTTPError for bad responses
            return response.text
        except requests.exceptions.RequestException as e:
            logging.error(f"Error during M3U playlist retrieval: {e}")
            return None

def save_streams_to_csv(streams_data, categories, category_type, csv_filename, timestamp):
    """
    Saves stream data to a CSV file with specified column order, 
    date/time conversion, and category name.

    Args:
        streams_data: A list of dictionaries, where each dictionary represents a stream.
        categories: A list of dictionaries representing categories.
        category_type: The type of category ('live', 'vod', or 'series').
        csv_filename: The base name of the CSV file to create (without extension).
        timestamp: A formatted timestamp string to append to the filename.
    """
    if not streams_data:
        logging.warning(f"No {category_type} stream data to save.")
        return

    try:
        # Create a dictionary to map category IDs to category names
        category_id_to_name = {
            cat["category_id"]: cat["category_name"] for cat in categories
        }

        # Define the desired column order based on category type
        if category_type == "live":
            ordered_fieldnames = [
                "category_name",
                "name",
                "num",
                "stream_icon",
                "epg_channel_id",
                "is_adult",
            ]
        elif category_type == "vod":
            ordered_fieldnames = [
                "category_name",
                "name",
                "stream_id",
                "rating",
                "added",
                "stream_icon",
            ]
        elif category_type == "series":
            ordered_fieldnames = [
                "category_name",
                "name",
                "series_id",
                "rating",
                "cast",
                "director",
                "genre",
                "plot",
                "cover",
            ]
        else:
            ordered_fieldnames = []

        # Find all other fields not in the ordered list
        remaining_fieldnames = set()
        for stream in streams_data:
            remaining_fieldnames.update(stream.keys())
        remaining_fieldnames = remaining_fieldnames - set(ordered_fieldnames)

        # Combine ordered fields with the rest of the fields (sorted alphabetically)
        fieldnames = ordered_fieldnames + sorted(list(remaining_fieldnames))

        # Add UTC timestamp to filename
        csv_filename = f"{csv_filename}_{timestamp}.csv"

        with open(csv_filename, 'w', newline="", encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            for stream in streams_data:
                # Convert "added" timestamp to ISO format where present
                if "added" in stream:
                    try:
                        added_timestamp = int(stream.get("added", 0))
                        added_datetime = datetime.fromtimestamp(
                            added_timestamp, tz=timezone.utc
                        ).isoformat()
                        stream["added"] = added_datetime
                    except ValueError:
                        logging.warning(
                            f"Could not convert 'added' field for stream: {stream.get('name', 'N/A')}"
                        )

                # Add category name
                category_id = stream.get("category_id")
                stream["category_name"] = category_id_to_name.get(category_id, "N/A")

                # Remove stream_id from series and live data if present
                if "stream_id" in stream and category_type != "vod":
                    del stream["stream_id"]

                writer.writerow(stream)

        logging.info(f"{category_type.capitalize()} stream data saved to {csv_filename}")

    except Exception as e:
        logging.error(f"Error saving {category_type} stream data to CSV: {e}")

def load_config(config_filename):
    """
    Loads Xtream Codes provider details from a YAML config file.

    Args:
        config_filename: The path to the YAML config file.

    Returns:
        A dictionary containing the provider details, or None if an error occurs.
    """
    try:
        with open(config_filename, "r") as f:
            config = yaml.safe_load(f)
        return config
    except Exception as e:
        logging.error(f"Error loading config from {config_filename}: {e}")
        return None

# Example Usage:
config_filename = "providers.yaml"  # Replace with your config file name

# Load provider details from config file
config = load_config(config_filename)

# Get the current timestamp in UTC
current_datetime_utc = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")

if config and "providers" in config:
    for provider in config["providers"]:
        provider_name = provider["name"]
        api_base_url = provider["url"]
        username = provider["username"]
        password = provider["password"]

        logging.info(f"Processing provider: {provider_name}")

        # Create a client for the current provider
        client = XtreamCodesAPI(api_base_url, username, password)

        # Get live streams
        live_streams = client.get_live_streams()
        if not live_streams:
            logging.error(f"Error: No live streams found for {provider_name} or error in API request.")
        live_categories = client.get_live_categories()
        if not live_categories:
            logging.error(f"Error: No live categories found for {provider_name} or error in API request.")

        if live_streams and live_categories:
            csv_filename = f"{provider_name}_live_streams"
            save_streams_to_csv(
                live_streams,
                live_categories,
                "live",
                csv_filename,
                current_datetime_utc,
            )

        # Get VOD streams
        vod_streams = client.get_vod_streams()
        if not vod_streams:
            logging.error(f"Error: No VOD streams found for {provider_name} or error in API request.")
        vod_categories = client.get_vod_categories()
        if not vod_categories:
             logging.error(f"Error: No VOD categories found for {provider_name} or error in API request.")
        
        if vod_streams and vod_categories:
            csv_filename = f"{provider_name}_vod_streams"
            save_streams_to_csv(
                vod_streams,
                vod_categories,
                "vod",
                csv_filename,
                current_datetime_utc,
            )

        # Get series streams
        series_streams = client.get_series()
        if not series_streams:
            logging.error(f"Error: No series streams found for {provider_name} or error in API request.")
        series_categories = client.get_series_categories()
        if not series_categories:
            logging.error(f"Error: No series categories found for {provider_name} or error in API request.")

        if series_streams and series_categories:
            csv_filename = f"{provider_name}_series_streams"
            save_streams_to_csv(
                series_streams,
                series_categories,
                "series",
                csv_filename,
                current_datetime_utc,
            )
else:
    logging.error("Invalid or missing 'providers' section in the config file.")