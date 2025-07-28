from flask import Flask, render_template, request, redirect, session
import json
import os

app = Flask(__name__)
app.secret_key = 'secret123'  # For session handling

# Base directory (for file path safety)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
QUESTIONS_PATH = os.path.join(BASE_DIR, 'mcqs', 'questions.json')

# 🔐 Password page (Handles both GET and POST)
@app.route('/', methods=['GET', 'POST'])
def password():
    if request.method == 'POST':
        if request.form.get('password') == '123':
            session['authenticated'] = True
            return redirect('/test')
        else:
            return render_template('password.html', error="❌ Incorrect password")
    return render_template('password.html')

# 📄 Test page (only accessible after login)
@app.route('/test')
def test():
    if not session.get('authenticated'):
        return redirect('/')
    with open(QUESTIONS_PATH, 'r', encoding='utf-8') as f:
        questions = json.load(f)
    return render_template('test.html', questions=questions)

# ✅ Result page (after submission)
@app.route('/submit', methods=['POST'])
def submit():
    if not session.get('authenticated'):
        return redirect('/')
    with open(QUESTIONS_PATH, 'r', encoding='utf-8') as f:
        questions = json.load(f)

    results = []

    for q in questions:
        qid = str(q["id"])
        correct_ans = q["answer"]
        selected_ans = request.form.get(qid)

        result = {
            "question": q["question"],
            "correct": [correct_ans],
            "selected": [selected_ans] if selected_ans else [],
            "is_correct": selected_ans == correct_ans
        }
        results.append(result)

    return render_template('result.html', results=results)

# 🚀 Run the app
if __name__ == '__main__':
    app.run(debug=True)
