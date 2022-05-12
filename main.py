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
print(country_map)
df.Country = df.Country.map(country_map)

print(df.Country.value_counts())

fig, ax = plt.subplots(1, 1, figsize = (12, 7))
df.boxplot('Salary', 'Country', ax = ax)
plt.suptitle('Salary (US$) v Country')
plt.title('')
plt.ylabel('Salary')
plt.xlabel('Country')
plt.xticks(rotation = 90)
# plt.show()

# Now that we see the outliers for each data, we want to exclude those with salary that is too low or too high that can skew our calculations
# Since USA has the most data point, I decide to find the mean salary of those from that country to set the upper limit
print(df[df.Country == 'United States of America'].Salary.median())
df = df[df['Salary'] <= df[df.Country == 'United States of America'].Salary.median()]
df = df[df['Salary'] >= 10000]
df = df[df['Country'] != 'Other']
fig, ax = plt.subplots(1, 1, figsize = (12, 7))
df.boxplot('Salary', 'Country', ax = ax)
plt.suptitle('Salary (US$) v Country')
plt.title('')
plt.ylabel('Salary')
plt.xlabel('Country')
plt.xticks(rotation = 90)
# plt.show()
# Now we see fewer outliers in our data set

print(df["YearsOfExp"].unique())

def convert_exp(num):
    if num == 'More than 50 years':
        return 50
    if num == 'Less than 1 year':
        return 0.5
    return float(num)
# Convert string to float
df['YearsOfExp'] = df['YearsOfExp'].apply(convert_exp)
