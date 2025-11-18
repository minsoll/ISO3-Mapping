import pandas as pd
import re
from fuzzywuzzy import process

# Function to normalize country names for better matching
def normalize(text):
    text = str(text).lower().strip()  # Convert to lowercase and remove leading/trailing spaces
    text = re.sub(r'\(.*?\)', '', text)  # Remove content inside parentheses
    text = re.sub(r'[^a-z0-9 ]', '', text)  # Remove special characters
    text = re.sub(r'\bthe\b', '', text)  # Remove the word 'the'
    return text.strip()

# Load the ILO unemployment dataset (19th ICLS definition)
id24 = pd.read_excel("id=24.xlsx")

# Load the country reference table (from Navicat)
country = pd.read_excel("country.xlsx")

# Normalize both long and short country names for matching
country['norm_long'] = country['longName_EN'].apply(normalize)
country['norm_short'] = country['shortName_EN'].apply(normalize)

# Create a list of all normalized country names (long + short)
all_names = pd.concat([country['norm_long'], country['norm_short']]).dropna().unique()

# Function to match a country name from the ILO dataset to an ISO3 code
def match_iso3(area):
    norm_area = normalize(area)

    # Manual override for Czechia
    if norm_area == "czechia":
        return "CZE"

    # Fuzzy match against normalized country names
    match, score = process.extractOne(norm_area, all_names)

    # If the match score is high enough, return the corresponding ISO3 code
    if score >= 90:
        row = country[(country['norm_long'] == match) | (country['norm_short'] == match)]
        if not row.empty:
            return row['ISO3Code'].values[0]

    # Return None if no good match is found
    return None

# Apply the matching function to the 'Area' column to assign ISO3 codes
id24['ISO3Code'] = id24['Area'].apply(match_iso3)

# Save the result to a new Excel file
id24.to_excel("id=24_with_fuzzy_ISO3.xlsx", index=False)
