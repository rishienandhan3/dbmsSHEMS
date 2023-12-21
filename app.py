from flask import Flask, redirect, url_for, render_template, flash, session, request
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

# create a Flask App instance:
app = Flask(__name__)
app.config['SECRET_KEY'] = "b\xe2\xd3&\xb0\x03n\x9c!\x153NX"


# Database connection function
def get_db_connection():
    connection = sqlite3.connect('shems.db')
    connection.row_factory = sqlite3.Row
    # cursor.execute('')
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
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        phone = request.form['phone']

        unit = request.form['unit']
        street = request.form['street']
        house_num = request.form['house_num']
        city = request.form['city']
        state = request.form['state']
        zip = request.form['zip']

        connection = get_db_connection()
        cursor = connection.cursor()

        hashed_password = generate_password_hash(password, method='pbkdf2')

        cursor.execute('INSERT INTO User (username, password, first_name, last_name, email, phone) VALUES (?, ?, ?, ?, ?, ?)', (username, hashed_password, first_name, last_name, email, phone))
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
            session['user_id'] = user['username']
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Login failed. Check your username and password.', 'danger')

    return render_template('login.html')


# Route for the user dashboard
@app.route('/dashboard')
def dashboard():
    if 'user_id' in session:
        # Implement your dashboard logic here
        return render_template('dashboard.html')
    else:
        return redirect(url_for('login'))


# Route for user logout
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('home'))


# Route for adding a new service location
@app.route('/add_location', methods=['GET', 'POST'])
def add_location():
    if 'user_id' in session:
        if request.method == 'POST':
            user_id = session['user_id']
            address_id = request.form['address_id']
            move_in_date = request.form['move_in_date']
            square_footage = request.form['square_footage']
            bedrooms = request.form['bedrooms']
            occupants = request.form['occupants']

            connection = get_db_connection()
            cursor = connection.cursor()

            cursor.execute(
                'INSERT INTO ServiceLocation (UserID, AddressID, move_in_date, square_footage, bedrooms, occupants) VALUES (?, ?, ?, ?, ?, ?)',
                (user_id, address_id, move_in_date, square_footage, bedrooms, occupants)
            )
            connection.commit()
            connection.close()

            flash('Service location added successfully!', 'success')
            return redirect(url_for('dashboard'))

        return render_template('add_location.html')
    else:
        return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
