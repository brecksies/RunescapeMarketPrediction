import requests
import os
from dotenv import load_dotenv

load_dotenv()

discordUser = os.getenv("DISCORD_USER")

endpoints = {
    "OSRS": "prices.runescape.wiki/api/v1/osrs",
    "DMM": "prices.runescape.wiki/api/v1/dmm"
}
endpoint_paths = ["5m", "1h", "latest", "mapping", "timeseries"]
timestepOptions = ["5m", "1h", "6h", "24h"]


def get_timeseries_data(game_mode="OSRS", item_id=None, timestep="5m", timestamp=None):
    return get_market_data(game_mode=game_mode, endpoint_path="timeseries", item_id=item_id, timestep=timestep, timestamp=timestamp)

def get_market_data(game_mode="OSRS", endpoint_path = "", item_id=None, timestep=None, timestamp=None):
    if game_mode not in endpoints:
        raise ValueError(f"Invalid game mode. Choose {endpoints.keys}.")
    endpoint = endpoints[game_mode]

    match (endpoint_path):
        case "5m" | "1h" | "latest" | "mapping":
            endpoint += f"/{endpoint_path}"
            if timestep is not None:
                raise ValueError(f"Timestep and timestamp parameters are not applicable for {endpoint_path} endpoint.")
        case "timeseries":
            if timestep not in timestepOptions:
                raise ValueError(f"Invalid timestep. Choose from {timestepOptions}.")
            if item_id is None:
                raise ValueError("Item ID must be provided for timeseries endpoint.")
            endpoint += "/timeseries"
        case _:
            raise ValueError(f"Invalid endpoint path. Choose from {endpoint_paths}.")

    params = {"useragent": f"Market Data ML - Discord @{discordUser}"}
    if item_id is not None:
        params['id'] = item_id
    if timestep is not None:
        params['timestep'] = timestep
    if timestamp is not None:
        params['timestamp'] = timestamp

    response = requests.get(endpoint, params=params)
    response.raise_for_status()  # Raise an error for bad responses

    return response.json()



