from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from models.database import db, User, Subject, Chapter, Quiz, Questions, Score
from controllers.config import AdminCredentials
from datetime import datetime


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'randomstring'
db.init_app(app)

@app.route("/")

def login():
    return render_template("LOGIN.html")

@app.route("/admin")
def admin():
    subjects = Subject.query.all()
    chapters = Chapter.query.all()
    return render_template("admin.html", subjects=subjects, chapters=chapters)


@app.route("/", methods=["POST"])
def verify_admin():
    username = request.form["email_id"]
    password = request.form["password"]

    if username == AdminCredentials.get_username() and password == AdminCredentials.get_password():
        return admin()
    
    user = User.query.filter_by(email=username, password=password).first()
    if user:
        session["user_id"] = user.user_id
        flash("Login successful!", "success")
        return redirect(url_for("user_detail", user_id=user.user_id))
    else:
        flash("Access Denied!", "Failed")
        return redirect("/")
    
@app.route("/user/<int:user_id>")
def user_detail(user_id):
    user = User.query.get(user_id)
    quizzes = Quiz.query.all()
    
    quiz_total_marks = {}
    for quiz in quizzes:
        total_marks = sum(question.marks for question in quiz.questions)
        quiz_total_marks[quiz.quiz_id] = total_marks

    return render_template('user_detail.html', user=user, quizzes=quizzes, user_id=user_id, quiz_total_marks=quiz_total_marks)


@app.route("/New-User", methods=["GET", "POST"])
def new_user():
    if request.method == "POST":
        user = User(
            email=request.form["email_id"],
            password=request.form["password"],
            full_name=request.form["full-name"],
            qualification=request.form["qulify"],
            dob=datetime.strptime(request.form["DOB"], "%Y-%m-%d")
        )
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("user_detail", user_id=user.user_id))

    return render_template("New-User.html")

    
@app.route("/subjects", methods=["GET", "POST"])
def subjects():
    if request.method == "POST":
        subject_name = request.form["subject_name"]
        subject_discription = request.form["subject_discription"]
        new_subject = Subject(subject_name=subject_name, subject_discription=subject_discription)
        db.session.add(new_subject)
        db.session.commit()
        return admin()
    all_subjects = Subject.query.all()
    return render_template("admin.html", subjects=all_subjects)

@app.route("/delete-subject/<int:subject_id>")
def delete_subject(subject_id):
    subject = Subject.query.get_or_404(subject_id)
    Chapter.query.filter_by(subject_id=subject_id).delete()
    if subject:
        db.session.delete(subject)
        db.session.commit()

    return redirect(url_for("subjects"))

@app.route("/chapters", methods=["POST"])
def add_chapter():
    if request.method == "POST":
        chapter_name = request.form["chapter_name"]
        chapter_discription = request.form["chapter_discription"]
        subject_id = request.form["subject_id"]
        new_chapter = Chapter(chapter_name=chapter_name, subject_id=subject_id, chapter_discription=chapter_discription)
        db.session.add(new_chapter)
        db.session.commit()
        flash("Chapter deleted successfully!", "success")
        return admin()
    all_chapters = Chapter.query.all()
    return render_template("admin.html", chapters = all_chapters)

@app.route("/delete-chapter/<int:id>")
def delete_chapter(id):
    chapter = Chapter.query.get_or_404(id)
    if chapter:
        db.session.delete(chapter)
        db.session.commit()
        flash("Chapter deleted successfully!", "success")

    return redirect(url_for("subjects"))


@app.route("/Create_quiz", methods = ["Get", "Post"])
def create_quiz():
    if request.method == "POST":
        chapter_id = request.form["chapter_id"]
        quiz_name = request.form["quiz_name"]
        date_of_quiz = datetime.strptime(request.form["date"], "%Y-%m-%d")
        time_duration = int(request.form["time_duration"])
        new_quiz = Quiz(chapter_id = chapter_id, quiz_name = quiz_name, date_of_quiz = date_of_quiz, time_duration = time_duration)
        db.session.add(new_quiz)
        db.session.commit()
        flash("Quiz addes successfully!", "success")
        return quiz()
    all_quizes = Quiz.query.all()
    return render_template("Quiz.html", quizzes = all_quizes)

@app.route("/questions", methods = ["GET","POST"])
def add_question():
    if request.method == "POST":
        quiz_id = request.form["quiz_id"]
        question_statement = request.form["question_statement"]
        option_1 = request.form["option_1"]
        option_2 = request.form["option_2"]
        option_3 = request.form["option_3"]
        option_4 = request.form["option_4"]
        correct_option = request.form["correct_option"]
        marks = int(request.form["marks"])
        new_question = Questions(quiz_id = quiz_id, question_statement = question_statement, option_1 = option_1, option_2 = option_2, option_3 = option_3, option_4 = option_4, marks = marks, correct_option = correct_option)
        db.session.add(new_question)
        db.session.commit()
        flash("Question added successfully!", "success")
        return quiz()
    all_questions = Questions.query.all()
    return render_template("Quiz.html", questions = all_questions)
    
@app.route('/delete_quiz/<int:quiz_id>')
def delete_quiz(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    Questions.query.filter_by(quiz_id=quiz_id).delete()
    db.session.delete(quiz)
    db.session.commit()
    flash("Quiz and its questions deleted successfully!", "success")
    return redirect(url_for('quiz'))

@app.route('/delete_question/<int:question_id>')
def delete_question(question_id):
    question = Questions.query.get_or_404(question_id)
    db.session.delete(question)
    db.session.commit()
    flash("Question deleted successfully!", "success")
    return redirect(url_for('quiz'))

@app.route("/quiz")
def quiz():
    chapters = Chapter.query.all()
    quizzes = Quiz.query.all()
    questions = Questions.query.all()
    return render_template("Quiz.html", chapters = chapters, quizzes = quizzes, questions = questions)


@app.route("/summary", methods=["GET"])
def summary():
    search_query = request.args.get('query', '').lower()

    users = User.query.all()
    subjects = Subject.query.all()
    chapters = Chapter.query.all()
    quizzes = Quiz.query.all()
    questions = Questions.query.all()
    search_results = {"users": users, "subjects": subjects, "chapters": chapters, "quizzes": quizzes, "questions": questions}

    if search_query:
        def matches(item, fields):
            for field in fields:
                if search_query in str(getattr(item, field)).lower():
                    return True
            return False

        search_results = {
            "users": [user for user in users if matches(user, ['full_name', 'email'])],
            "subjects": [subject for subject in subjects if matches(subject, ['subject_name', 'subject_discription'])],
            "chapters": [chapter for chapter in chapters if matches(chapter, ['chapter_name', 'chapter_discription'])],
            "quizzes": [quiz for quiz in quizzes if matches(quiz, ['quiz_name'])],
            "questions": [question for question in questions if matches(question, ['question_statement'])],
        }

    return render_template("summary.html", search_results=search_results, users=users, subjects=subjects, chapters=chapters, quizzes=quizzes, questions=questions)



@app.route("/scores/<int:user_id>")
def scores(user_id):
    user = User.query.get(user_id)
    scores = Score.query.filter_by(user_id=user_id).all() 
    
    score_details = []
    for score in scores:
        quiz = Quiz.query.get(score.quiz_id)
        chapter = Chapter.query.get(quiz.chapter_id)
        subject = Subject.query.get(chapter.subject_id)

        
        total_marks = sum(question.marks for question in quiz.questions)

        score_details.append({'quiz_name': quiz.quiz_name, 'chapter_name': chapter.chapter_name, 'subject_name': subject.subject_name, 'score': score.score, 'total_marks': total_marks
        })
    
    return render_template("scores.html", user=user, user_id=user_id, score_details=score_details)

@app.route('/start_quiz/<int:quiz_id>/<int:user_id>', methods=['GET'])
def start_quiz(quiz_id, user_id):
    quiz = Quiz.query.get(quiz_id)
    time_duration = quiz.time_duration
    user = User.query.get(user_id)
    questions = Questions.query.filter_by(quiz_id=quiz_id).order_by(Questions.question_id).all()
    
    #if Score.query.filter_by(user_id=user_id, quiz_id=quiz_id).first():
        #flash("You've already attempted this quiz!", "warning")
        #return redirect(url_for('user_detail', user_id=user_id))

    return render_template('Quiz_page.html', quiz=quiz, user=user, user_id=user_id, questions=questions, time_duration=time_duration)

@app.route("/submit_quiz/<int:quiz_id>/<int:user_id>", methods=["POST"])
def submit_quiz(quiz_id, user_id):
    existing_score = Score.query.filter_by(user_id=user_id, quiz_id=quiz_id).first()
    #if existing_score:
        #flash("You've already taken this quiz!", "warning")
        #return redirect(url_for('user_detail', user_id=user_id))

    score = 0
    quiz = Quiz.query.get(quiz_id)
    questions = Questions.query.filter_by(quiz_id=quiz_id).all()
    
    for question in questions:
        answer_key = f"question_{question.question_id}"
        user_answer = request.form.get(answer_key)
        if user_answer and user_answer == str(question.correct_option):
            score += question.marks

    total_possible = sum(q.marks for q in questions)
    new_score = Score(
        user_id=user_id,
        quiz_id=quiz_id,
        score=score,
        total_marks=total_possible,
        attempt_date=datetime.now()
    )
    
    db.session.add(new_score)
    db.session.commit()

    flash(f"Quiz submitted! Your score: {score}/{total_possible}", "success")
    return redirect(url_for('scores', user_id=user_id))



@app.route("/user_summary/<int:user_id>")
def user_summary(user_id):
    user = User.query.get(user_id)
    search_query = request.args.get('query', '').lower()

    
    scores = Score.query.filter_by(user_id=user_id).all()
    all_quizzes = Quiz.query.all()

    
    score_details = []
    available_quizzes = []

    for score in scores:
        quiz = Quiz.query.get(score.quiz_id)
        chapter = Chapter.query.get(quiz.chapter_id)
        subject = Subject.query.get(chapter.subject_id)
        total_marks = sum(q.marks for q in quiz.questions)
        score_details.append({
            'quiz_name': quiz.quiz_name,
            'chapter_name': chapter.chapter_name,
            'subject_name': subject.subject_name,
            'score': score.score,
            'total_marks': total_marks,
            'date': score.attempt_date
        })

    for quiz in all_quizzes:
        
        if not Score.query.filter_by(user_id=user_id, quiz_id=quiz.quiz_id).first():
            chapter = Chapter.query.get(quiz.chapter_id)
            subject = Subject.query.get(chapter.subject_id)
            total_marks = sum(q.marks for q in quiz.questions)
            available_quizzes.append({
                'quiz_name': quiz.quiz_name,
                'chapter_name': chapter.chapter_name,
                'subject_name': subject.subject_name,
                'total_marks': total_marks,
                'quiz_id': quiz.quiz_id,
                'date': quiz.date_of_quiz
            })

    
    if search_query:
        score_details = [score for score in score_details if 
            search_query in score['quiz_name'].lower() or
            search_query in score['chapter_name'].lower() or
            search_query in score['subject_name'].lower()]

        available_quizzes = [quiz for quiz in available_quizzes if 
            search_query in quiz['quiz_name'].lower() or
            search_query in quiz['chapter_name'].lower() or
            search_query in quiz['subject_name'].lower()]

    return render_template("user_summary.html", user=user, user_id=user_id, score_details=score_details, available_quizzes=available_quizzes, search_query=search_query)

if __name__ == "__main__":
    with app.app_context():
        db.create_all() 
    app.run(debug=True) 