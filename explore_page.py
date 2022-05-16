import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st


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
    df.Country = df.Country.map(country_map)
    df = df[df['Salary'] <= df[df.Country == 'United States of America'].Salary.median()]
    df = df[df['Salary'] >= 10000]
    df = df[df['Country'] != 'Other']
    # Convert string type to float
    df['YearsOfExp'] = df['YearsOfExp'].apply(convert_exp)
    # reclassify education level for simplicity
    df['EdLevel'] = df['EdLevel'].apply(clean_edu)

    return df

df = load_data()

def show_explore_page():
    st.title("Explore Software Engineer Salaries")

    st.write(
        """
        ### Stack Overflow Developer Survey 2021
        """
    )

    data = df["Country"].value_counts()
    fig1, ax1 = plt.subplots()
    ax1.pie(data, labels=data.index, autopct="%1.1f%%", shadow = True, startangle = 90, textprops={'size': 'smaller'}, explode=(0.15, 0.15, 0.15, 0.15,0.15,0.15,0.15,0.15,0.15,0.15,0.15,0.15,0.15,0.15,0.15,0.15,0.15,0.15))
    ax1.axis("equal") # Equal aspect ratio ensures that pie is drawn as a circle
    st.write("""#### Number of Data from different countries""")
    st.write("""*Only countries with more than or equal to 400 surveys are shown""")


    st.pyplot(fig1)