#Quiz Master

Here’s how to run your Flask application step by step:

### Prerequisites:
1. **Python 3.x** installed.
2. **Flask** and **SQLAlchemy** installed.
3. **SQLite** installed (if not using a pre-configured database).

---

### Step 1: Install Dependencies  
Run the following command to install Flask and SQLAlchemy:  
```bash
pip install Flask Flask-SQLAlchemy
```

---

### Step 2: Project Structure  
Ensure your project files are organized as follows:
```
project/
├── app.py              # Main Flask application
├── models/
│   └── database.py      # Database models
├── controllers/
│   └── config.py        # Admin credentials
├── templates/           # HTML templates
│   ├── LOGIN.html
│   ├── admin.html
│   ├── user_detail.html
│   ├── New-User.html
│   ├── Quiz.html
│   ├── Quiz_page.html
│   ├── scores.html
│   ├── summary.html
│   └── user_summary.html
└──instance/
   |
   -- database.db          # SQLite database file
```


### Step 3: Admin Credential
Email_id: 23f3004461@ds.study.iitm.ac.in
Password: 23f3004461


### Step 3: Run the Flask Application  
Run the application using:
```shell
python app.py
```
This will start the server at:
```
http://127.0.0.1:5000/
```


### Step 4: Access the App  
1. **Login Page:**  
   Visit the root URL:  
   ```
   http://127.0.0.1:5000/
   ```
   Enter admin credentials or create a new user.

2. **Admin Dashboard:**  
   After successful login as admin, manage subjects, chapters, quizzes, and questions.

3. **User Dashboard:**  
   After user login, view quizzes, scores, and available quizzes.


### Step 5: Taking a Quiz  
1. Start a quiz by clicking the **Start Quiz** button.  
2. Answer the questions and submit.  
3. View your score and details on the **Score Summary** page.


### Step 6: Admin Functions  
- Add subjects, chapters, and quizzes.  
- Add or delete questions.  
- View the list of quizzes and users.

