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