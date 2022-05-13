import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error
import numpy as np
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import GridSearchCV

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

# Now that we see the outliers for each data, we want to exclude those with salary that is too low or too high that can skew our predictions
# Since USA has the most data point, I decide to find the median salary of those from the country to set the upper limit
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

# print(df["YearsOfExp"].unique())

def convert_exp(num):
    if num == 'More than 50 years':
        return 50
    if num == 'Less than 1 year':
        return 0.5
    return float(num)
# Convert string to float
df['YearsOfExp'] = df['YearsOfExp'].apply(convert_exp)

# print(df.EdLevel.unique())

def clean_edu(x):
    if 'Bachelor’s degree' in x:
        return 'Bachelor’s degree'
    if 'Master’s degree' in x:
        return 'Master’s degree'
    if 'Professional degree' in x or 'Other doctoral' in x:
        return 'Post Grad'
    return 'Less than a Bachelors'

# reclassify education level for simplicity
df['EdLevel'] = df['EdLevel'].apply(clean_edu)

# Use Label Encoder to transform string data to what computer can interpret which is numbers
le = LabelEncoder()

df['EdLevel'] = le.fit_transform(df['EdLevel'])
# print(df.EdLevel.unique())

df['Country'] = le.fit_transform(df['Country'])
# print(df.Country.unique())

# Separate features and label
x = df.drop('Salary', axis = 1)
y = df['Salary']
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size= 0.1)


linear = LinearRegression()
linear.fit(x_train, y_train)
accuracy = linear.score(x_test, y_test)
# We can see that our model accuracy is very low
print("Accuracy Percentage for Linear Regression: ", format(accuracy, "%"))
# When calculating the error, we can see model predict off by approx $26791
y_pred = linear.predict(x_test)
error = np.sqrt(mean_squared_error(y_test, y_pred))
print("${:,.02f}".format(error))

# Now I choose Decision Tree Regressor as the new model
dec_tree_reg = DecisionTreeRegressor(random_state=0)
dec_tree_reg.fit(x_train, y_train)
accuracy = dec_tree_reg.score(x_test, y_test)
# We can see that our model accuracy is now a bit higher but it's still not enough
print("Accuracy Percentage for Decision Tree Regressor: ", format(accuracy, "%"))
y_pred = dec_tree_reg.predict(x_test)
error = np.sqrt(mean_squared_error(y_test, y_pred))
print("${:,.02f}".format(error))

max_depth = [None, 2,4,6,8,10,12]
parameters = {"max_depth" : max_depth}

regressor = DecisionTreeRegressor(random_state=0)
gs = GridSearchCV(regressor, parameters, scoring = 'neg_mean_squared_error')
gs.fit(x_train, y_train)
regressor = gs.best_estimator_
regressor.fit(x_train, y_train)
accuracy = regressor.score(x_test, y_test)
# We can see that our model accuracy is now a bit higher but it's still not enough
print("Accuracy Percentage for Decision Tree Regressor after tuning: ", format(accuracy, "%"))
y_pred = regressor.predict(x_test)
error = np.sqrt(mean_squared_error(y_test, y_pred))
print("${:,.02f}".format(error))

# Now I choose Random Forest Regressor
random_forest_reg = RandomForestRegressor(random_state=0)
random_forest_reg.fit(x_train, y_train)
accuracy = random_forest_reg.score(x_test, y_test)
print("Accuracy Percentage for Random Forest Regressor: ", format(accuracy, "%"))
y_pred = random_forest_reg.predict(x_test)
error = np.sqrt(mean_squared_error(y_test, y_pred))
print("${:,.02f}".format(error))



parameters = {"max_depth" : [None, 2,4,6,8,10,12],
              "max_features" : ["sqrt", "log2", None],
              "n_estimators" : [100,140,160,180,200,300]}

regressor = RandomForestRegressor(random_state=0)
gs = GridSearchCV(regressor, parameters, scoring = 'neg_mean_squared_error', verbose=True)
gs.fit(x_train, y_train)
regressor = gs.best_estimator_
regressor.fit(x_train, y_train)
accuracy = regressor.score(x_test, y_test)
# We can see that our model accuracy is now a bit higher but it's still not enough
print("Accuracy Percentage for Random Forest Regressor after tuning: ", format(accuracy, "%"))
y_pred = regressor.predict(x_test)
error = np.sqrt(mean_squared_error(y_test, y_pred))
print("${:,.02f}".format(error))

# country, edLevel, yearsOfExp
x_test = np.array([["United States", "Master's degree", 15]])
x_test[:, 0] = le.transform(x_test[:, 0])
x_test[:, 0] = le.transform(x_test[:, 1])