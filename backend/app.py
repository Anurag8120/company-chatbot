from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from chatbot import ask_question

app = Flask(__name__)
CORS(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    if not data or "message" not in data:
        return jsonify({"error": "No message provided"}), 400

    user_message = data["message"].strip()
    if not user_message:
        return jsonify({"response": "Please type a question."})

    response = ask_question(user_message)
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)
