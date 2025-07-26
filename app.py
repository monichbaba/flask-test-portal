from flask import Flask, render_template, request, redirect, url_for, session
import json

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for session

# Load questions
with open('questions.json', encoding='utf-8') as f:
    questions = json.load(f)

# Password to access test
TEST_PASSWORD = "test123"  # You can change this

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        password = request.form['password']
        if password == TEST_PASSWORD:
            session['authenticated'] = True
            return redirect(url_for('test'))
        else:
            return render_template('password.html', error="Galat password")
    return render_template('password.html')

@app.route('/test', methods=['GET', 'POST'])
def test():
    if not session.get('authenticated'):
        return redirect(url_for('login'))

    if request.method == 'POST':
        user_answers = {}
        results = []

        for q in questions:
            qid = str(q['id'])
            selected = request.form.getlist(qid)
            correct = q['answer']
            is_correct = set(selected) == set(correct)
            results.append({
                'question': q['question'],
                'options': q['options'],
                'selected': selected,
                'correct': correct,
                'is_correct': is_correct
            })
        return render_template('result.html', results=results)

    return render_template('test.html', questions=questions)

@app.route('/logout')
def logout():
    session.pop('authenticated', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
