import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


def shorten_categories(categories, cutoff):
    categorical_map = {}
    for i in range(len(categories)):
        if categories.values[i] >= cutoff:
            categorical_map[categories.index[i]] = categories.index[i]
        else:
            categorical_map[categories.index[i]] = 'Other'

    return categorical_map

def convert_exp(num):
    if num == 'More than 50 years':
        return 50
    if num == 'Less than 1 year':
        return 0.5
    return float(num)

def clean_edu(x):
    if 'Bachelor’s degree' in x:
        return 'Bachelor’s degree'
    if 'Master’s degree' in x:
        return 'Master’s degree'
    if 'Professional degree' in x or 'Other doctoral' in x:
        return 'Post Grad'
    return 'Less than a Bachelor'

# Cache the data so it won't have to reload
@st.cache
def load_data():
    df = pd.read_csv('data/survey_results_public.csv')
    # Only get the columns that are needed for our model
    df = df[["Employment", "Country", "EdLevel", "ConvertedCompYearly", "YearsCodePro"]]
    # Rename the columns with more intuitive naming
    df = df.rename({"ConvertedCompYearly": "Salary", "YearsCodePro": "YearsOfExp"}, axis=1)
    # Drop all the rows that contains missing data
    df = df.dropna()
    # Only collect data with people of full time employment
    df = df[df["Employment"] == "Employed full-time"]
    # After that, drop the column, since we no longer need it
    df = df.drop("Employment", axis=1)

    country_map = shorten_categories(df.Country.value_counts(), 400)
    df = df[df['Salary'] <= df[df.Country == 'United States of America'].Salary.median()]
    df = df[df['Salary'] >= 10000]
    df = df[df['Country'] != 'Other']
    # Convert string type to float
    df['YearsOfExp'] = df['YearsOfExp'].apply(convert_exp)
    # reclassify education level for simplicity
    df['EdLevel'] = df['EdLevel'].apply(clean_edu)

    return df

df = load_data()
