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
            selected = request.form.getlist(f'q{i}')
            selected_indices = sorted([int(x) for x in selected])
            correct_indices = sorted(q['answer'])
            is_correct = selected_indices == correct_indices
            if is_correct:
                score += 1
            result.append({
                "q": q['q'],
                "options": q['options'],
                "selected": selected_indices,
                "correct": correct_indices,
                "is_correct": is_correct
            })
        return render_template('result.html', score=score, total=len(questions), result=result)

    return render_template('test.html', questions=questions)

if __name__ == '__main__':
    app.run(debug=True)
