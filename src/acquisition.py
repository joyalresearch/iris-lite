import os
from pathlib import Path

import requests
from dotenv import load_dotenv

def get_cdse_access_token(env_path=".env"):
    """Authenticate with Copernicus Data Space and return an access token."""

    load_dotenv(env_path)

    username = os.environ["CDSE_USERNAME"]
    password = os.environ["CDSE_PASSWORD"]

    auth_url = (
        "https://identity.dataspace.copernicus.eu/"
        "auth/realms/CDSE/protocol/openid-connect/token"
    )

    auth_data = {
        "client_id": "cdse-public",
        "grant_type": "password",
        "username": username,
        "password": password,
    }

    response = requests.post(auth_url, data=auth_data)
    response.raise_for_status()

    return response.json()["access_token"]

def search_stac(
    collection,
    bbox,
    datetime_range,
    cloud_cover=None,
    limit=100
):
    """Search the CDSE STAC catalogue and return matching Items."""

    search_url = "https://stac.dataspace.copernicus.eu/v1/search"

    params = {
        "collections": [collection],
        "bbox": bbox,
        "datetime": datetime_range,
        "limit": limit,
    }

    if cloud_cover is not None:
        params["query"] = {
            "eo:cloud_cover": {
                "lte": cloud_cover
            }
        }

    response = requests.post(search_url, json=params)
    response.raise_for_status()

    data = response.json()

    return data["features"]

def select_item_by_tile(items, tile_id):
    """Select a STAC Item containing the requested MGRS tile ID."""

    matches = [
        item for item in items
        if item["properties"].get("grid:code") == tile_id
    ]

    if not matches:
        raise ValueError(f"No Item found for tile {tile_id}")

    if len(matches) > 1:
        raise ValueError(
            f"Multiple Items found for tile {tile_id}; "
            "additional selection criteria are required."
        )

    return matches[0]

def get_asset_url(item, asset_key):
    """Return the authenticated HTTPS URL for a STAC Asset."""
    return item["assets"][asset_key]["alternate"]["https"]["href"]

def download_asset(url, output_path, token):
    """Download an authenticated CDSE asset to disk."""

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    headers = {
        "Authorization": f"Bearer {token}"
    }

    with requests.get(
        url,
        headers=headers,
        stream=True
    ) as response:

        response.raise_for_status()

        with open(output_path, "wb") as file:
            for chunk in response.iter_content(chunk_size=1024 * 1024):
                if chunk:
                    file.write(chunk)

    return output_path