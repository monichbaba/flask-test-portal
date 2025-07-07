from flask import Flask, render_template, request
import os
import json

app = Flask(__name__)

# 📁 Test List Page
@app.route("/")
def home():
    qsets = []
    for filename in os.listdir("mcqs"):
        if filename.endswith(".json"):
            qsets.append(filename[:-5])
    return render_template("index.html", qsets=qsets)

# 📄 Test Attempt Page
@app.route("/test/<qset>")
def test(qset):
    file_path = f"mcqs/{qset}.json"
    if not os.path.exists(file_path):
        return "❌ Test not found."

    with open(file_path, "r", encoding="utf-8") as f:
        questions = json.load(f)

    return render_template("test.html", questions=questions, qset=qset)

# 📤 Test Submission + Score Page
@app.route("/submit", methods=["POST"])
def submit():
    qset = request.form.get("qset")
    file_path = f"mcqs/{qset}.json"
    
    if not os.path.exists(file_path):
        return "❌ Invalid qset name."

    with open(file_path, "r", encoding="utf-8") as f:
        questions = json.load(f)

    score = 0
    result = []

    for i, q in enumerate(questions):
        key = f"q{i}"
        selected_raw = request.form.get(key)

        # Default is None if user skipped
        if selected_raw is not None and selected_raw.isdigit():
            selected_index = int(selected_raw)
        else:
            selected_index = None

        correct_index = q["answer_index"]

        # ✅ Count only if selected is not None and correct
        if selected_index is not None and selected_index == correct_index:
            score += 1

        result.append({
            "q": q["q"],
            "options": q["options"],
            "selected": selected_index,
            "correct_index": correct_index
        })

    return render_template("result.html", score=score, total=len(questions), result=result)

# 🚫 Remove app.run() for Render
# if __name__ == "__main__":
#     app.run(debug=True)
