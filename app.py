from flask import Flask, render_template, request
import json, os

app = Flask(__name__)
app.jinja_env.globals.update(enumerate=enumerate)

@app.route('/', methods=['GET', 'POST'])
def test():
    filepath = 'mcqs/today.json'
    if not os.path.exists(filepath):
        return "❌ File mcqs/today.json not found"

    with open(filepath, encoding='utf-8') as f:
        questions = json.load(f).get('questions', [])

    if request.method == 'POST':
        result = []
        score = 0
        for i, q in enumerate(questions):
            sel = request.form.get(f'q{i}')
            idx = int(sel) if sel and sel.isdigit() else -1
            correct_idx = q['options'].index(q['answer'])
            if idx == correct_idx:
                score += 1
            result.append({
                "q": q['q'],
                "options": q['options'],
                "correct_index": correct_idx,
                "selected": idx
            })
        return render_template('result.html', score=score, total=len(questions), result=result)

    return render_template('test.html', questions=questions)

if __name__ == '__main__':
    app.run(debug=True)
