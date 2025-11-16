from flask import Flask, render_template, request, jsonify
import openai

app = Flask(__name__)

# usually i wouldnt hardcode an api key but this is just for the project
openai.api_key = "OPENAI_API_KEY"

CANNED_QUESTIONS = [
    "What events are happening this week?",
    "Tell me about student organization fairs.",
    "When is the next club meeting?"
]

@app.route("/")
def index():
    return render_template("index.html", canned_questions=CANNED_QUESTIONS)

@app.route("/ask", methods=["POST"])
def ask():
    user_input = request.json.get("question")
    if not user_input:
        return jsonify({"answer": "Please provide a question."})
# {"role": "system", "content": "You are a helpful assistant for student events. Answer questions briefly (under 100 words). Introduce yourself as the UniMatch assistant"},

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant for student events. Answer questions VERY briefly (under 30 words if possible). Introduce yourself as the UniMatch assistant"},
                {"role": "user", "content": user_input}
            ],
            max_tokens=200
        )
        # Old syntax for version 0.28.x
        answer = response.choices[0].message["content"].strip()
    except Exception as e:
        answer = f"Error: {str(e)}"

    return jsonify({"answer": answer})

@app.route("/feedback", methods=["POST"])
def feedback():
    data = request.get_json()
    message_id = data.get("message_id")
    feedback_type = data.get("feedback")

    print(f"Feedback received — ID: {message_id}, Feedback: {feedback_type}")

    return jsonify({"status": "success"})

if __name__ == "__main__":
    app.run(debug=True)

