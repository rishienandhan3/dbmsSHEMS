from flask import Flask, redirect, url_for, render_template, flash, session, request
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

# create a Flask App instance:
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # Replace with a secret key for session management

# # SQLite database connection
# DATABASE = 'your_database_name.db'
# conn = sqlite3.connect(DATABASE)
# cursor = conn.cursor()
# Database connection function
def get_db_connection():
    connection = sqlite3.connect('database.db')
    connection.row_factory = sqlite3.Row
    return connection

@app.route('/')
def home():
    return render_template("index.html")


# Route to render the registration form
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        connection = get_db_connection()
        cursor = connection.cursor()

        hashed_password = generate_password_hash(password, method='sha256')

        cursor.execute('INSERT INTO User (username, password) VALUES (?, ?)', (username, hashed_password))
        connection.commit()
        connection.close()

        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')

# Route to render the login form
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        connection = get_db_connection()
        cursor = connection.cursor()

        user = cursor.execute('SELECT * FROM User WHERE username = ?', (username,)).fetchone()

        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Login failed. Check your username and password.', 'danger')

    return render_template('login.html')


# Route for the user dashboard
@app.route('/dashboard')
def dashboard():
    # Render the user dashboard with energy consumption views
    # ...

# Route for user logout
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
