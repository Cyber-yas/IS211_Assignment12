from flask import Flask, render_template, request, redirect, url_for, flash, g
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for flashing messages

DATABASE = 'hw13.db'  # Your SQLite database file

# Function to get the database connection
def get_db():
    db = sqlite3.connect(DATABASE)
    return db

# Route for login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username == 'admin' and password == 'password':
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials, please try again.')
            return redirect(url_for('login'))
    return render_template('login.html')

# Route for dashboard
@app.route('/dashboard')
def dashboard():
    db = get_db()
    students = db.execute('SELECT * FROM students').fetchall()
    quizzes = db.execute('SELECT * FROM quizzes').fetchall()
    return render_template('dashboard.html', students=students, quizzes=quizzes)

# Route to add a student
@app.route('/student/add', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        
        db = get_db()
        db.execute('INSERT INTO students (first_name, last_name) VALUES (?, ?)', (first_name, last_name))
        db.commit()
        
        return redirect(url_for('dashboard'))
    
    return render_template('add_student.html')

# Route to add a quiz
@app.route('/quiz/add', methods=['GET', 'POST'])
def add_quiz():
    if request.method == 'POST':
        subject = request.form['subject']
        question_count = request.form['question_count']
        quiz_date = request.form['quiz_date']
        
        db = get_db()
        db.execute('INSERT INTO quizzes (subject, question_count, quiz_date) VALUES (?, ?, ?)', (subject, question_count, quiz_date))
        db.commit()
        
        return redirect(url_for('dashboard'))
    
    return render_template('add_quiz.html')

# Route to add quiz result
@app.route('/results/add', methods=['GET', 'POST'])
def add_result():
    db = get_db()
    students = db.execute('SELECT * FROM students').fetchall()
    quizzes = db.execute('SELECT * FROM quizzes').fetchall()
    
    if request.method == 'POST':
        student_id = request.form['student_id']
        quiz_id = request.form['quiz_id']
        score = request.form['score']
        
        db.execute('INSERT INTO quiz_results (student_id, quiz_id, score) VALUES (?, ?, ?)', (student_id, quiz_id, score))
        db.commit()
        
        return redirect(url_for('dashboard'))
    
    return render_template('add_result.html', students=students, quizzes=quizzes)

# Route to view student's quiz results
@app.route('/student/<int:id>')
def student_results(id):
    db = get_db()
    results = db.execute('SELECT * FROM quiz_results WHERE student_id = ?', (id,)).fetchall()
    return render_template('student_results.html', results=results, student_id=id)

if __name__ == '__main__':
    app.run(debug=True)
