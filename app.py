from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)

PASSWORD = "mahadev"

with open('mcqs/questions.json', 'r', encoding='utf-8') as f:
    questions = json.load(f)

@app.route('/')
def password():
    return render_template('password.html')

@app.route('/verify', methods=['POST'])
def verify():
    password = request.form.get('password')
    if password == PASSWORD:
        return redirect(url_for('test'))
    return "Wrong password", 403

@app.route('/test')
def test():
    return render_template('test.html', questions=questions)

@app.route('/submit', methods=['POST'])
def submit():
    user_answers = {}
    correct_answers = {}
    results = []

    for q in questions:
        qid = str(q['id'])
        selected = request.form.getlist(f"q{qid}")
        user_answers[qid] = selected
        correct_answers[qid] = q['answer']

        # Compare sets
        is_correct = set(selected) == set(q['answer'])
        results.append({
            'question': q['question'],
            'your_answers': [q['options'][opt] for opt in selected],
            'correct_answers': [q['options'][opt] for opt in q['answer']],
            'is_correct': is_correct
        })

    return render_template('result.html', results=results)

if __name__ == '__main__':
    app.run(debug=True)
