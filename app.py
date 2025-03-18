import os
import streamlit as st
import requests
import pandas as pd
import numpy as np
import nltk

nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)
nltk.download('wordnet', quiet=True)

# STEP 1:
# ASK FOR USER-INPUT TEXT TO DETERMINE MOOD

# STEP 4:
# DISPLAY ON THE SCREEN RECOMMENDED BOOKS

# App's NLP model
google_api_key = os.environ.get("API_KEY")

backend_url = os.environ.get("BACKEND_URL")

# Design app's interface
def main():
    st.title("Welcome to your personal Book Recommendation System")
    
    selected_genres = st.multiselect("Select genres", ["Fiction", "Mystery", "Romance", "Fantasy", 
                                                   "Science", "History", "Autobiography"])

    st.write("### How are you feeling today?")
    user_text = st.text_area("Describe your mood or what kind of story you're looking for...", 
                           height=150)
    
    if st.button("Find Books For My Mood"):
        if user_text:
            with st.spinner("Analyzing your mood and finding perfect book matches..."):
                # Get user mood profile
                response = requests.post(backend_url, json={"mood_text" : user_text})
                
                if response.status_code == 200:
                    data = response.json()
                    
                    # Display mood analysis
                    st.write("### 🧠 Your Mood Profile")
                    st.write(f"**Predicted Mood:** {data['mood_profile']}")
                    
                    # Display book recommendations
                    st.write("### Your Recommended Books")
                    
                    # Display books in a grid (2 columns)
                    if data["recommendations"]:
                        cols = st.columns(2)
                        for i, book in enumerate(data["recommendations"]):
                            col = cols[i % 2]
                            with col:
                                st.subheader(book['title'])
                                col2 = st.columns([3])
                                with col2:
                                    st.write(f"**Author:** {book['author']}")
                                    st.write(f"**Mood match:** {book.get('similarity_score', 0):.0%}")
                                    st.write(book['description'][:150] + "...")
                                    st.write("---")
                    else:
                        st.warning("No books match your mood!")
                else:
                    st.warning("Please describe your mood first!")


if __name__ == "__main__":
    main()