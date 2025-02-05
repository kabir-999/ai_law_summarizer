import pandas as pd
import pickle
from flask import Flask, render_template, request, jsonify
from sklearn.metrics.pairwise import cosine_similarity
from fuzzywuzzy import process

app = Flask(__name__)

# Load dataset
df = pd.read_csv("data/legal_acts_dataset.csv")  
df["Act Name"] = df["Act Name"].str.lower()
df["AI Summary"] = df["AI Summary"].str.lower()

# Load TF-IDF Vectorizer and Matrix
with open("models/tfidf_vectorizer.pkl", "rb") as f:
    vectorizer = pickle.load(f)

with open("models/tfidf_matrix.pkl", "rb") as f:
    tfidf_matrix = pickle.load(f)

# Function to find the closest Act Name
def get_closest_act_name(user_input):
    best_match_tuple = process.extractOne(user_input, df["Act Name"])
    if best_match_tuple:
        best_match, confidence = best_match_tuple[:2]
        if confidence > 80:
            return best_match
    return None  

# Function to predict summary based on Act Name
def get_summary(act_input):
    act_input = act_input.lower()
    
    corrected_act_name = get_closest_act_name(act_input)
    if corrected_act_name:
        print(f"✅ Corrected Act Name: {corrected_act_name}")  
    else:
        corrected_act_name = act_input  

    input_vec = vectorizer.transform([corrected_act_name])
    similarities = cosine_similarity(input_vec, tfidf_matrix)
    best_match_index = similarities.argmax()
    return df.iloc[best_match_index]["AI Summary"]

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get_summary", methods=["GET"])
def fetch_summary():
    act_name = request.args.get("act_name")
    if not act_name:
        return jsonify({"error": "Please provide an 'act_name' parameter"}), 400

    summary = get_summary(act_name)
    return jsonify({"act_name": act_name, "ai_summary": summary})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
