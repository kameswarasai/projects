from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    email = db.Column(db.String(70), unique = True, nullable = False)
    password = db.Column(db.String(100), nullable = False)
    full_name = db.Column(db.String(50), nullable = False)
    qualification = db.Column(db.String(20), nullable = False)
    dob = db.Column(db.Date, nullable = False)
    scores = db.relationship('Score', backref='user', lazy=True)

class Subject(db.Model):
    subject_id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    subject_name = db.Column(db.String(100), nullable = False)
    subject_discription = db.Column(db.String(500), nullable = False)
    chapters = db.relationship('Chapter', backref='subject', lazy=True)

class Chapter(db.Model):
    chapter_id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    chapter_name = db.Column(db.String(100), nullable = False)
    chapter_discription = db.Column(db.String(500), nullable = False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.subject_id'))
    quizzes = db.relationship('Quiz', backref='chapter', lazy=True)

class Quiz(db.Model):
    quiz_id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    quiz_name = db.Column(db.String(100), nullable = False)
    chapter_id = db.Column(db.Integer, db.ForeignKey('chapter.chapter_id'))
    date_of_quiz = db.Column(db.Date, nullable = False)
    time_duration = db.Column(db.Integer, nullable = False)
    questions = db.relationship('Questions', backref='quiz', lazy=True)

class Questions(db.Model):
    question_id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.quiz_id'))
    question_statement = db.Column(db.String(400), nullable = False)
    option_1 = db.Column(db.String(200), nullable = False)
    option_2 = db.Column(db.String(200), nullable = False)
    option_3 = db.Column(db.String(200), nullable = False)
    option_4 = db.Column(db.String(200), nullable = False)
    correct_option = db.Column(db.String(200), nullable = False)
    marks = db.Column(db.Integer, nullable = False)

class Score(db.Model):
    score_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.quiz_id'))
    score = db.Column(db.Integer, nullable=False)
    total_marks = db.Column(db.Integer, nullable=False)
    attempt_date = db.Column(db.DateTime, nullable=False)