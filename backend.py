from flask import Flask, request, jsonify
import torch
import os
from langchain_groq import ChatGroq

app = Flask(__name__)



def generate_response(prompt, api_key):
    try:
        os.environ["GROQ_API_KEY"] = api_key  # Set the API key dynamically
        model = ChatGroq(model="llama3-8b-8192")
        response = model.invoke(prompt).content
        return response
    except Exception as e:
        return f"Error: {str(e)}"

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_input = data.get("message", "")
    api_key = data.get("api_key", "")

    if not api_key:
        return jsonify({"reply": "API Key is required"}), 400

    response = generate_response(user_input, api_key)
    return jsonify({"reply": response})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
