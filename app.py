import streamlit as st
from predict_page import show_predict_page

# Create a side bar where we can toggle between explore and predict page
st.sidebar.selectbox("Explore Or Predict", ("Predict", "Explore"))
show_predict_page()

