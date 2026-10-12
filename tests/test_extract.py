import pytest
from unittest.mock import patch
import pandas as pd
from extract import return_dataframe, get_access_token
import os

@patch('extract.requests.post')
def test_get_access_token_success(mock_post):
    os.environ['SPOTIFY_CLIENT_ID'] = 'dummy_id'
    os.environ['SPOTIFY_CLIENT_SECRET'] = 'dummy_secret'
    os.environ['SPOTIFY_REFRESH_TOKEN'] = 'dummy_token'

    mock_response = mock_post.return_value
    mock_response.status_code = 200
    mock_response.json.return_value = {"access_token": "mocked_token"}

    token = get_access_token()
    assert token == "mocked_token"

@patch('extract.requests.post')
def test_get_access_token_failure(mock_post):
    os.environ['SPOTIFY_CLIENT_ID'] = 'dummy_id'
    os.environ['SPOTIFY_CLIENT_SECRET'] = 'dummy_secret'
    os.environ['SPOTIFY_REFRESH_TOKEN'] = 'dummy_token'

    mock_response = mock_post.return_value
    mock_response.status_code = 400
    mock_response.text = "Bad Request"

    token = get_access_token()
    assert token is None

@patch('extract.get_access_token')
@patch('extract.requests.get')
def test_return_dataframe_success(mock_get, mock_get_token):
    mock_get_token.return_value = "mocked_token"

    mock_response = mock_get.return_value
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "items": [
            {
                "track": {
                    "name": "Song 1",
                    "album": {"artists": [{"name": "Artist 1"}]}
                },
                "played_at": "2023-01-01T12:00:00Z"
            }
        ]
    }

    df = return_dataframe()

    assert not df.empty
    assert len(df) == 1
    assert df.iloc[0]["song_name"] == "Song 1"
    assert df.iloc[0]["artist_name"] == "Artist 1"
    assert df.iloc[0]["played_at"] == "2023-01-01T12:00:00Z"
    assert df.iloc[0]["timestamp"] == "2023-01-01"

@patch('extract.get_access_token')
def test_return_dataframe_no_token(mock_get_token):
    mock_get_token.return_value = None

    df = return_dataframe()
    assert df.empty
