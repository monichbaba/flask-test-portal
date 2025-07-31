from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)

# ✅ Password protection
PASSWORD = "123"  # Change if needed

# ✅ Password page
@app.route('/', methods=['GET', 'POST'])
def password():
    if request.method == 'POST':
        entered_password = request.form['password']
        if entered_password == PASSWORD:
            return redirect(url_for('test'))
        else:
            return render_template('password.html', error="Invalid password")
    return render_template('password.html')

# ✅ Test page with questions
@app.route('/test')
def test():
    with open('mcqs/questions.json', 'r', encoding='utf-8') as f:
        questions = json.load(f)
    return render_template('test.html', questions=questions)

# ✅ Result page logic
@app.route('/submit', methods=['POST'])
def submit():
    with open('mcqs/questions.json', 'r', encoding='utf-8') as f:
        questions = json.load(f)

    results = []
    for q in questions:
        qid = str(q['id'])
        correct_option_key = q['answer']  # "A", "B", "C", "D"
        selected_option_key = request.form.get(qid)

        selected_text = q['options'].get(selected_option_key, "No Answer Selected")
        correct_text = q['options'].get(correct_option_key, "N/A")

        results.append({
            'question': q['question'],
            'correct_answer_text': correct_text,
            'your_answer_text': selected_text,
            'is_correct': selected_option_key == correct_option_key
        })

    return render_template('result.html', results=results)

if __name__ == '__main__':
    app.run(debug=True)
