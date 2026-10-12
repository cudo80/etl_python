import pytest
import pandas as pd
from transform import data_quality, transform_df

def test_data_quality_empty_df():
    empty_df = pd.DataFrame()
    assert data_quality(empty_df) == False

def test_data_quality_duplicates():
    df = pd.DataFrame({
        "song_name": ["Song A", "Song A"],
        "artist_name": ["Artist A", "Artist A"],
        "played_at": ["2023-01-01T12:00:00Z", "2023-01-01T12:00:00Z"],
        "timestamp": ["2023-01-01", "2023-01-01"]
    })
    with pytest.raises(Exception, match="Primary Key Exception,Data Might Contain duplicates"):
        data_quality(df)

def test_data_quality_nulls():
    df = pd.DataFrame({
        "song_name": ["Song A", None],
        "artist_name": ["Artist A", "Artist B"],
        "played_at": ["2023-01-01T12:00:00Z", "2023-01-01T13:00:00Z"],
        "timestamp": ["2023-01-01", "2023-01-01"]
    })
    with pytest.raises(Exception, match="Null values found"):
        data_quality(df)

def test_transform_df():
    df = pd.DataFrame({
        "song_name": ["Song A", "Song B", "Song C"],
        "artist_name": ["Artist A", "Artist A", "Artist B"],
        "played_at": ["2023-01-01T10:00:00Z", "2023-01-01T11:00:00Z", "2023-01-01T12:00:00Z"],
        "timestamp": ["2023-01-01", "2023-01-01", "2023-01-01"]
    })

    transformed = transform_df(df)

    assert len(transformed) == 2
    assert "count" in transformed.columns
    assert "ID" in transformed.columns

    # Check Artist A count
    artist_a = transformed[transformed["artist_name"] == "Artist A"].iloc[0]
    assert artist_a["count"] == 2
    assert artist_a["ID"] == "2023-01-01-Artist A"
