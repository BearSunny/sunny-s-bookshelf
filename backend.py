from flask import Flask, request, jsonify
import requests
import pandas as pd
import os
import nltk

nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)
nltk.download('wordnet', quiet=True)

mood_api_url = os.environ.get("MOOD_API_URL")

# STEP 3:
# PREDICTED MOOD IS THEN MATCHED TO 10 BOOKS
# THEN FEED THIS TO app.py

app = Flask(__name__)

# Load book data once
books_df = pd.read_csv("books_with_profiles.csv")

def analyze_mood(user_text):
    response = requests.post(mood_api_url, json={"text": user_text})
    if response.status_code == 200:
        return response.json().get("mood", "neutral")
    return "neutral"

def find_matching_books(books_df, mood, top_n=10):
    return books_df[books_df["mood"] == mood].head(top_n)

@app.route('/recommend', methods=['POST'])
def recommend():
    data = request.json
    user_text = data.get("mood_text", "")

    if not user_text:
        return jsonify({"error": "Mood text is required"}), 400

    user_profile = analyze_mood(user_text)
    matches = find_matching_books(books_df, user_profile, top_n=10)

    recommendations = matches.to_dict(orient="records")

    return jsonify({
        "mood_profile": user_profile,
        "recommendations": recommendations
    })

if __name__ == '__main__':
    app.run(debug=True)
