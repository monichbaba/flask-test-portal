from flask import Flask, render_template, request, redirect, url_for, session
import json
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# ✅ Questions file ka correct path
file_path = os.path.join(os.path.dirname(__file__), 'mcqs', 'questions.json')
with open(file_path, encoding='utf-8') as f:
    questions = json.load(f)

# ✅ Home page
@app.route('/')
def index():
    return render_template('index.html')

# ✅ Password screen (GET + POST both allowed)
@app.route('/password', methods=['GET', 'POST'])
def password():
    if request.method == 'POST':
        entered_password = request.form.get('password')
        if entered_password == 'admin':
            session['authenticated'] = True
            return redirect(url_for('test'))
        else:
            return render_template('password.html', error='Galat password hai')
    return render_template('password.html')

# ✅ Quiz page
@app.route('/test', methods=['GET', 'POST'])
def test():
    if not session.get('authenticated'):
        return redirect(url_for('password'))

    if request.method == 'POST':
        answers = request.form
        score = 0
        results = []

        for i, q in enumerate(questions):
            user_ans = answers.get(f'q{i}')
            correct = q['answer']
            results.append({
                'question': q['question'],
                'options': q['options'],
                'user': user_ans,
                'correct': correct,
                'is_correct': user_ans == correct
            })
            if user_ans == correct:
                score += 1

        return render_template('result.html', results=results, score=score, total=len(questions))

    return render_template('test.html', questions=questions)

# ✅ Local run (not used in Render, but useful for dev)
if __name__ == '__main__':
    app.run(debug=True)
