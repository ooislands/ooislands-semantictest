from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Needed for session management

# Define the questions and scale labels
questions = [
    {"id": "q1", "label": "자주 읽음", "opposite": "거의 읽지 않음"},
    {"id": "q2", "label": "즐거움", "opposite": "불쾌함"},
    {"id": "q3", "label": "가벼운 독서", "opposite": "깊이 있는 독서"},
    {"id": "q4", "label": "소설", "opposite": "비소설"},
    {"id": "q5", "label": "빠름", "opposite": "느림"},
    {"id": "q6", "label": "혼자 읽음", "opposite": "함께 읽음"},
    {"id": "q7", "label": "전자책", "opposite": "종이책"},
    {"id": "q8", "label": "계획적", "opposite": "즉흥적"},
    {"id": "q9", "label": "편안함", "opposite": "스트레스 받음"},
    {"id": "q10", "label": "낮 시간", "opposite": "밤 시간"}
]

complementary_characters = {
    "Avid Reader": "Casual Reader",
    "Casual Reader": "Avid Reader",
    "Night Owl": "Early Bird",
    "Early Bird": "Night Owl",
    "Digital Reader": "Print Lover",
    "Print Lover": "Digital Reader",
    "Social Reader": "Solitary Reader",
    "Solitary Reader": "Social Reader",
    "The Dreamer": "The Realist",
    "The Realist": "The Dreamer",
    "Undefined": "Undefined"
}

@app.route('/')
def index():
    return redirect(url_for('question', q_num=1))

@app.route('/question/<int:q_num>', methods=['GET', 'POST'])
def question(q_num):
    if request.method == 'POST':
        if 'back' in request.form:
            return redirect(url_for('question', q_num=q_num - 1))
        else:
            for question in questions:
                if question['id'] in request.form:
                    response = request.form[question['id']]
                    session[question['id']] = response
            if q_num < len(questions):
                return redirect(url_for('question', q_num=q_num + 1))
            else:
                return redirect(url_for('results'))
    
    progress = int((q_num - 1) / len(questions) * 100)
    return render_template('question.html', question=questions[q_num - 1], q_num=q_num, progress=progress)

@app.route('/results')
def results():
    results = {q['id']: int(session.get(q['id'], '4')) for q in questions}  # Default to neutral value 4
    user_character = analyze_results(results)
    complementary_character = complementary_characters.get(user_character, "Undefined")
    return render_template('results.html', results=results, questions=questions, user_character=user_character, complementary_character=complementary_character)

def analyze_results(results):
    # Priority-based categorization for assigning a single dominant reader character
    if results['q10'] >= 5:
        return "Night Owl"
    elif results['q10'] <= 3:
        return "Early Bird"
    
    if results['q7'] <= 3:
        return "Digital Reader"
    elif results['q7'] >= 5:
        return "Print Lover"
    
    if results['q6'] >= 5:
        return "Social Reader"
    elif results['q6'] <= 3:
        return "Solitary Reader"
    
    if results['q4'] <= 3:
        return "The Dreamer"
    elif results['q4'] >= 5:
        return "The Realist"
    
    if results['q1'] <= 3 and results['q2'] <= 3:
        return "Avid Reader"
    elif results['q1'] <= 5 and results['q2'] <= 5:
        return "Casual Reader"

    return "Undefined"

if __name__ == '__main__':
    app.run(debug=True)