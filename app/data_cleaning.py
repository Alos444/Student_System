

import pandas as pd
import difflib

from flask import jsonify, app


def correct_city_names(df):
    """
    Correct city names in the DataFrame using approximate string matching.
    """
    # Get unique city names from the DataFrame
    unique_cities = df['city'].unique()

    # Create a dictionary to store corrected city names
    corrections = {}

    # Iterate over unique city names
    for city in unique_cities:
        # Find the most similar city name within the dataset
        match = difflib.get_close_matches(city, unique_cities, n=1, cutoff=0.8)  # Adjust the cutoff as needed
        if match:
            corrections[city] = match[0]

    # Replace city names in the DataFrame with corrected names

    df['city'] = df['city'].replace(corrections)


    return df

def clean_data(file):
    """
    Read the CSV file, perform cleaning operations, and return a cleaned DataFrame.
    """
    # Read the CSV file into a DataFrame
    df = pd.read_csv(file)

    # Correct city names
    df = correct_city_names(df)

    # Drop duplicates, if any
    df = df.drop_duplicates()
    # Rename columns to replace periods with underscores
    df.rename(columns=lambda x: x.replace('.', '_'), inplace=True)

    return df

def main():
    # Load and clean the dataset
    cleaned_df = clean_data("student-dataset.csv")

    # save the cleaned dataset to a new CSV file
    cleaned_df.to_csv("cleaned_student_dataset.csv", index=False)


if __name__ == "__main__":
    main()



