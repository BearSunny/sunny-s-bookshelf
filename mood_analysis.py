from flask import Flask, request, jsonify
import pickle
from sklearn.feature_extraction.text import CountVectorizer
import nltk
nltk.download('punkt')

# STEP 2:
# LOAD NLP MODEL TO PROCESS USER-INPUT TEXT INTO MOOD
# THEN FEED THIS TO backend.py

app = Flask(__name__)

# Load trained model and vectorizer
with open("emotion_model.pkl", "rb") as model_file:
    lr_model = pickle.load(model_file)
with open("vectorizer.pkl", "rb") as vec_file:
    vectorizer = pickle.load(vec_file)

@app.route("/analyze_mood", methods=["POST"])
def analyze_mood():
    data = request.json
    user_text = data.get("text", "")
    
    if not user_text:
        return jsonify({"error": "No text provided"}), 400
    
    text_vectorized = vectorizer.transform([user_text])
    prediction = lr_model.predict(text_vectorized)
    
    return jsonify({"mood": prediction[0]})

if __name__ == "__main__":
    app.run(debug=True)
