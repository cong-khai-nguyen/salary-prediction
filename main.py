import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('data/survey_results_public.csv')
# print(df.columns.sort_values())
# Only get the columns that are needed for our model
df = df[["Employment", "Country", "EdLevel", "ConvertedCompYearly", "YearsCodePro"]]
# Rename the columns with more intuitive naming
df = df.rename({"ConvertedCompYearly" : "Salary", "YearsCodePro" : "YearsOfExp"}, axis = 1)
print(df.info())

# Drop all the rows that contains missing data and reset the index
df = df.dropna()
# df = df[df["YearsOfExp"].notna()]
# print(df.isnull().sum())
# print(df)

# Only collect data with people of full time employment
df = df[df["Employment"] == "Employed full-time"]
# After that, drop the column, since we no longer need it
df = df.drop("Employment", axis = 1)
print(df.info())

print(df["Country"].value_counts())

def shorten_categories(categories, cutoff):
    categorical_map = {}

    for i in range(len(categories)):
        if categories.values[i] >= cutoff:
            categorical_map[categories.index[i]] = categories.index[i]
        else:
            categorical_map[categories.index[i]] = 'Other'

    return categorical_map

country_map = shorten_categories(df.Country.value_counts(), 400)
df.Country = df.Country.map(country_map)

print(df.Country.value_counts())