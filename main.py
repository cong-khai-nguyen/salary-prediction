import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('data/survey_results_public.csv')
# print(df.columns.sort_values())
# Only get the columns that are needed for our model
df = df[["Employment", "Country", "EdLevel", "ConvertedCompYearly", "YearsCodePro"]]
df = df.rename({"ConvertedCompYearly" : "Salary"}, axis = 1).rename({"YearsCodePro" : "YearsOfExp"}, axis = 1)

# print(df.info())
print(df)