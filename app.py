import os
import streamlit as st
import pandas as pd
import numpy as np
import nltk

nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)
nltk.download('wordnet', quiet=True)

# App's NLP model
google_api_key = os.environ.get("API_KEY")

# Design app's interface
def main():
    st.title("Welcome to your personal Book Recommendation System")
    
    selected_genres = st.multiselect("Select genres", ["Fiction", "Mystery", "Romance", "Fantasy", 
                                                   "Science", "History", "Autobiography"])


if __name__ == "__main__":
    main()