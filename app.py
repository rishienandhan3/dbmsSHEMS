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


def get_next_user_id():
    connection = get_db_connection()
    cursor = connection.cursor()
    max_id = cursor.execute('SELECT MAX(UserID) FROM User').fetchone()[0]
    connection.commit()
    connection.close()
    if max_id is None:
        return 1
    else:
        return max_id + 1

def get_next_Address_id():
    connection = get_db_connection()
    cursor = connection.cursor()
    max_id = cursor.execute('SELECT MAX(AddressID) FROM Address').fetchone()[0]
    connection.commit()
    connection.close()
    if max_id is None:
        return 1
    else:
        return max_id + 1


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

        next_user_id = get_next_user_id()
        next_address_id = get_next_Address_id()
        cursor.execute('INSERT INTO User (UserID, first_name, last_name, email, username, password, phone, AddressID) VALUES (?, ?, ?, ?, ?, ?, ?, ?)', (next_user_id, first_name, last_name, email, username, hashed_password, phone, next_address_id))
        connection.commit()
        cursor.execute('INSERT INTO Address (AddressID, address_type, unit, street, house_num, city, state, zip) VALUES (?, ?, ?, ?, ?, ?, ?, ?)', (next_address_id, 'billing', unit, street, house_num, city, state, zip))
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
        connection = get_db_connection()
        cursor = connection.cursor()
        # Retrieve user's service locations
        locations = cursor.execute('SELECT * FROM ServiceLocation WHERE UserID = ?', ('user_id',)).fetchall()
        return render_template('dashboard.html', user_locations=locations)
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

            unit = request.form['unit']
            street = request.form['street']
            house_num = request.form['house_num']
            city = request.form['city']
            state = request.form['state']
            zip = request.form['zip']

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


# Route for enrolling devices in a service location
@app.route('/enroll_device/<int:location_id>', methods=['GET', 'POST'])
def enroll_device(location_id):
    if 'user_id' in session:
        user_id = session['user_id']
        connection = get_db_connection()
        cursor = connection.cursor()

        if request.method == 'POST':
            device_id = request.form['device_id']
            model_type = request.form['model_type']
            model_number = request.form['model_number']
            other_details = request.form['other_details']

            cursor.execute(
                'INSERT INTO EnrolledDevice (DeviceID, LocationID) VALUES (?, ?)',
                (device_id, location_id)
            )
            connection.commit()

            flash('Device enrolled successfully!', 'success')
            return redirect(url_for('dashboard'))

        connection.close()

        return render_template('enroll_device.html', location_id=location_id)
    else:
        return redirect(url_for('login'))


# Route for displaying enrolled devices in a service location
@app.route('/devices/<int:location_id>')
def devices(location_id):
    if 'user_id' in session:
        connection = get_db_connection()
        cursor = connection.cursor()

        # Retrieve enrolled devices for the specified location
        enrolled_devices = cursor.execute(
            'SELECT ed.*, dm.model_type, dm.model_number FROM EnrolledDevice ed '
            'JOIN DeviceModel dm ON ed.ModelID = dm.ModelID '
            'WHERE LocationID = ?',
            (location_id,)
        ).fetchall()

        connection.close()

        return render_template('devices.html', enrolled_devices=enrolled_devices)
    else:
        return redirect(url_for('login'))



if __name__ == '__main__':
    app.run(debug=True)
