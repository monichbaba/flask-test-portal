from flask import Flask, render_template, request
import json, os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def test():
    filepath = 'mcqs/today.json'
    if not os.path.exists(filepath):
        return "❌ mcqs/today.json file not found."

    with open(filepath, encoding='utf-8') as f:
        data = json.load(f)
        questions = data.get("questions", [])

    if request.method == 'POST':
        score = 0
        result = []
        for i, q in enumerate(questions):
            selected = request.form.get(f'q{i}')
            correct_index = q["options"].index(q["answer"])
            selected_index = int(selected) if selected and selected.isdigit() else -1
            if selected_index == correct_index:
                score += 1
            result.append({
                "q": q["q"],
                "options": q["options"],
                "correct_index": correct_index,
                "selected": selected_index
            })

        return render_template("result.html", score=score, total=len(questions), result=result)

    return render_template("test.html", questions=questions)
