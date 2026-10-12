import pandas as pd 
import requests
from datetime import datetime
import datetime
import os
import base64
from dotenv import load_dotenv
from logger_config import get_logger

logger = get_logger(__name__)

# Load environment variables
load_dotenv()

def get_access_token():
    """Generates a new access token using the refresh token."""
    CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
    CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
    REFRESH_TOKEN = os.getenv("SPOTIFY_REFRESH_TOKEN")

    if not all([CLIENT_ID, CLIENT_SECRET, REFRESH_TOKEN]):
        logger.error("Spotify credentials missing in environment variables.")
        return None

    auth_str = f"{CLIENT_ID}:{CLIENT_SECRET}"
    b64_auth_str = base64.b64encode(auth_str.encode()).decode()

    headers = {
        "Authorization": f"Basic {b64_auth_str}",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    data = {
        "grant_type": "refresh_token",
        "refresh_token": REFRESH_TOKEN
    }

    response = requests.post("https://accounts.spotify.com/api/token", headers=headers, data=data)

    if response.status_code == 200:
        return response.json().get("access_token")
    else:
        logger.error(f"Failed to refresh token: {response.text}")
        return None


# Creating an function to be used in other python files
def return_dataframe(): 
    token = get_access_token()
    if not token:
        logger.error("Could not obtain access token. Returning empty DataFrame.")
        return pd.DataFrame()

    input_variables = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
     
    today = datetime.datetime.now()
    yesterday = today - datetime.timedelta(days=5)
    yesterday_unix_timestamp = int(yesterday.timestamp()) * 1000

    # Download all songs you've listened to "after yesterday", which means in the last 24 hours      
    r = requests.get("https://api.spotify.com/v1/me/player/recently-played?limit=50&after={time}".format(time=yesterday_unix_timestamp), headers=input_variables)

    if r.status_code != 200:
        logger.error(f"Error extracting data from Spotify: {r.text}")
        return pd.DataFrame()

    data = r.json()
    song_names = []
    artist_names = []
    played_at_list = []
    timestamps = []

    # Extracting only the relevant bits of data from the json object      
    for song in data["items"]:
        song_names.append(song["track"]["name"])
        artist_names.append(song["track"]["album"]["artists"][0]["name"])
        played_at_list.append(song["played_at"])
        timestamps.append(song["played_at"][0:10])
        
    # Prepare a dictionary in order to turn it into a pandas dataframe below       
    song_dict = {
        "song_name": song_names,
        "artist_name": artist_names,
        "played_at": played_at_list,
        "timestamp": timestamps
    }
    song_df = pd.DataFrame(song_dict, columns=["song_name", "artist_name", "played_at", "timestamp"])
    return song_df


if __name__ == "__main__":
    df = return_dataframe()
    logger.info(f"Extracted Dataframe:\n{df}")
