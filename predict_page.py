import streamlit as st
import pickle
import numpy as np

def load_model():
    with open('saved_model.pickle', 'rb') as file:
        data = pickle.load(file)
    return data

data = load_model()
regressor = data['model']
le_country = data['le_country']
le_edu = data['le_edu']

def show_predict_page():
    st.title("Software Developer Salary Prediction")

    st.write("""### We need some information to predict the salary""")

    countries = {
        "United States of America",
        "India",
        "Germany",
        "United Kingdom of Great Britain and Northern Ireland",
        "Canada",
        "France",
        "Brazil",
        "Spain",
        "Netherlands",
        "Australia",
        "Poland",
        "Italy",
        "Russian Federation",
        "Sweden",
        "Turkey",
        "Switzerland",
        "Israel",
        "Norway"
    }
    education = {
        'Master’s degree',
        'Bachelor’s degree',
        'Post Grad',
        'Less than a Bachelor'
    }

    country = st.selectbox("Country", sorted(countries))
    education = st.selectbox("Education Level", sorted(education))

    experience = st.slider("Years of Experience", 0, 50, 3)

    clicked = st.button("Calculate Salary")

    if clicked:
      x = np.array([[country, education, experience]])
      # print(x)
      x[:,0] = le_country.transform(x[:, 0])
      x[:, 1] = le_edu.transform(x[:, 1])
      x = x.astype(float)
      predicted_salary = regressor.predict(x)
      print(predicted_salary)
      st.subheader(f"The estimated salary is ${predicted_salary[0]:.2f}")

