from flask import Flask, render_template, request, redirect, url_for, session
import os
import cv2
from flask import send_from_directory
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key'
UPLOAD_FOLDER = 'uploads'
STATIC_FOLDER = 'ststic' 
DB_FILE = 'users.db'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['STATIC_FOLDER'] = STATIC_FOLDER


def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()


def detect_artifacts(video_path):
    cap = cv2.VideoCapture(video_path)
    frame_count = 0
    total_blur_score = 0

    while frame_count < 30:
        ret, frame = cap.read()
        if not ret:
            break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blur_score = cv2.Laplacian(gray, cv2.CV_64F).var()
        total_blur_score += blur_score
        frame_count += 1

    cap.release()
    avg_blur = total_blur_score / frame_count if frame_count > 0 else 0
    return avg_blur < 100


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = generate_password_hash(request.form['password'])

        if not email.endswith("@gmail.com"):
            return render_template('signup_error.html', message="Only Gmail addresses are allowed!")

        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
                           (username, email, password))
            conn.commit()
        except sqlite3.IntegrityError:
            return render_template('signup_error.html', message="Username or Gmail already exists!")
        finally:
            conn.close()

        return render_template('signup_success.html', username=username)

    return render_template('signup.html')


@app.route('/')
def login_page():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT password FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()

    if user and check_password_hash(user[0], password):
        session['user'] = username
        return redirect('/home')
    else:
        return render_template('login_error.html')


@app.route('/home')
def home():
    if 'user' not in session:
        return redirect('/')
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload():
    if 'user' not in session:
        return redirect('/')

    video = request.files['video']
    if video:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], video.filename)
        video.save(filepath)

        result = detect_artifacts(filepath)
        message = "🛑 Deepfake Detected!" if result else "✅ Video Looks Real."
        return render_template('result.html', message=message)


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')


@app.route('/ststic/<path:filename>')
def serve_static(filename):
    return send_from_directory(app.config['STATIC_FOLDER'], filename)


if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    if not os.path.exists(STATIC_FOLDER):
        os.makedirs(STATIC_FOLDER)
    init_db()
    app.run(debug=True)
