import extract
import pandas as pd


# Set of Data Quality Checks Needed to Perform Before Loading
def data_quality(load_df):
    # Checking Whether the DataFrame is empty
    if load_df.empty:
        print('No Songs Extracted')
        return False

    # Enforcing Primary keys since we don't need duplicates
    if pd.Series(load_df['played_at']).is_unique:
        pass
    else:
        # The Reason for using exception is to immediately terminate the program and avoid further processing
        raise Exception("Primary Key Exception,Data Might Contain duplicates")

    # Checking for Nulls in our data frame
    if load_df.isnull().values.any():
        raise Exception("Null values found")


# Writing some Transformation Queries to get the count of artist
def transform_df(load_df):
    # Applying transformation logic
    transformed_df = load_df.groupby(['timestamp', 'artist_name'], as_index=False).count()
    transformed_df.rename(columns={'played_at': 'count'}, inplace=True)

    # Creating a Primary Key based on Timestamp and artist name
    transformed_df["ID"] = transformed_df['timestamp'].astype(str) + "-" + transformed_df["artist_name"]

    return transformed_df[['ID', 'timestamp', 'artist_name', 'count']]


if __name__ == "__main__":
    # Importing the songs_df from the Extract.py
    load_df = extract.return_dataframe()
    data_quality(load_df)
    # calling the transformation
    transformed_df = transform_df(load_df)
    print(transformed_df)
