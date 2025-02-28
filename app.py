from flask import Flask, request, render_template
from utils.question_handler import handle_question

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    question = request.form['question']
    answer = handle_question(question)
    return render_template('index.html', question=question, answer=answer)

if __name__ == '__main__':
    app.run(debug=True)