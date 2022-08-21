# Salary Prediction Engine
Web: https://share.streamlit.io/nguyencongkhai1407/salary-prediction/main/app.py

Google Collab Notebook: https://colab.research.google.com/drive/1nfWzFhaq45IVqtyp4WfFwlolt2bAiFGH#scrollTo=yiofWU3Alqt3

# Description
There are two parts to this project. First, I took the data, processed it and developed a regression model to predict user's data. Lastly, I designed a web application using streamlit and push my github folders to streamlit hosting cloud. 

[Survey Data](https://insights.stackoverflow.com/survey)

[Data Overview](https://insights.stackoverflow.com/survey/2021#overview)

[Streamlit Documentation on line_chart](https://docs.streamlit.io/library/api-reference/charts/st.line_chart)

[Guide to draw a pie chart](https://matplotlib.org/3.5.0/gallery/pie_and_polar_charts/pie_demo2.html)

[Streamlit Documentation on bar_chart](https://docs.streamlit.io/library/api-reference/charts/st.bar_chart)

# Install and Run the Project
This project requires to imported and installed libraries: pandas, numpy, pickle, matplotlib, streamlit and scikit-learn.

sqlite3: To implement SQLite database, and functions

csv: To use CSV-related function

matplotlib.pyplot: For data visualization

pandas: To use for data manipulation and analysis

numpy: To work with arrays

Seaborn: For data visualization

Linregress(scipy.stats): To run Linear Regression

statsmodels.formula.api: To use classes and functions for the estimation of, test statistical models

FuncAnimation(matplotlib.animation): To use function to draw a clear frame

HTML(IPython.display): To display media to the screen

SARIMAX(statsmodels.tsa.statespace.sarimax): To use and run ARMA model


# Errors that I encountered and found fix:
1. `streamlit : The term 'streamlit' is not recognized as the name of a cmdlet, function, script file, or operable program. Check  the spelling of the name, or if a path was included, verify that the path is correct and try again.`

    Solution: https://discuss.streamlit.io/t/getting-an-error-streamlit-is-not-recognized-as-an-internal-or-external-command-operable-program-or-batch-file/361/14

2. `ModuleNotFoundError: This app has encountered an error`

    Solution: https://discuss.streamlit.io/t/modulenotfounderror-this-app-has-encountered-an-error/23092
