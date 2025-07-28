from flask import Flask, render_template, request, redirect, session
import json
import os

app = Flask(__name__)
app.secret_key = 'secret123'  # Session secret

# ✅ Password page (GET + POST)
@app.route('/', methods=['GET', 'POST'])
def password():
    if request.method == 'POST':
        if request.form.get('password') == '123':
            session['authenticated'] = True
            return redirect('/test')
        else:
            return render_template('password.html', error="❌ Incorrect password")
    return render_template('password.html')

# ✅ Test page
@app.route('/test')
def test():
    if not session.get('authenticated'):
        return redirect('/')
    with open(os.path.join('mcqs', 'questions.json'), 'r', encoding='utf-8') as f:
        questions = json.load(f)
    return render_template('test.html', questions=questions)

# ✅ Submit answers and show result
@app.route('/submit', methods=['POST'])
def submit():
    if not session.get('authenticated'):
        return redirect('/')
    with open(os.path.join('mcqs', 'questions.json'), 'r', encoding='utf-8') as f:
        questions = json.load(f)

    results = []

    for q in questions:
        qid = str(q["id"])
        correct = q["answer"]
        selected = request.form.get(qid)

        results.append({
            "question": q["question"],
            "options": q["options"],
            "correct": correct,
            "selected": selected,
            "is_correct": selected == correct
        })

    return render_template('result.html', results=results)

# ✅ Run app
if __name__ == '__main__':
    app.run(debug=True)
