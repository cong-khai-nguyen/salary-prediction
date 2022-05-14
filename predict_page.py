import streamlit as st
import pickle
import numpy as np

def load_model():
    with open('saved_model.pickle', 'rb') as file:
        data = pickle.load()
    return data