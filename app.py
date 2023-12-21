from flask import Flask, redirect, url_for, render_template, flash, session, request
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

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


def get_next_DeviceID():
    connection = get_db_connection()
    cursor = connection.cursor()
    max_id = cursor.execute('SELECT MAX(DeviceID) FROM EnrolledDevice').fetchone()[0]
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
            session['user_id'] = user['UserID']
            session['username'] = user['username']
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
        locations = cursor.execute('SELECT * FROM ServiceLocation WHERE UserID = ?', (session['user_id'],)).fetchall()
        
        # Retrieve user's Energy Consumption Data in 4 ways and save to session
        # 1 Average Monthly Energy Consumption
        # months = ['01','02','03','04','05','06','07','08','09','10','11','12']
        # avg_monthly = []
        # for m in range(len(months) - 1):
        #     this_month = datetime.strptime('22/' + months[m] + '/01 00:00:00', '%y/%m/%d %H:%M:%S')
        #     next_month = datetime.strptime('22/' + months[m+1] + '/01 00:00:00', '%y/%m/%d %H:%M:%S')
        #     avg_monthly.append(cursor.execute("""WITH ActiveDevices AS (SELECT DISTINCT DeviceID FROM EnrolledDevice NATURAL JOIN EventData WHERE event_time >= '2022/"""+months[m]+"""/01 00:00:00' 
        #                                       AND """ + datetime.strptime(event_time)""" < ? AND label = 'Switched On')
        #                                       SELECT model_type, AVG(value) AS AvgMonthlyEnergyConsumption
        #                                       FROM DeviceModel NATURAL JOIN EnrolledDevice NATURAL JOIN ActiveDevices NATURAL JOIN EventData 
        #                                       WHERE event_time >= '2022/"""+months[m]+"""/01 00:00:00' AND event_time < '2022/"""+months[m+1]+"""/01 00:00:00' AND event_type = 'Energy Use'
        #                                       GROUP BY model_type;""", ()).fetchall())
        #     connection.commit()
        #     session['avg_monthly'] = avg_monthly
        # print(avg_monthly)

        # 2 Total Consumption per Location
        # total_cost_per_loc = cursor.execute("""SELECT LocationID, SUM(ed.value * ep.hourly_price)/100 AS total_cost_in_dollars
        #                                     FROM EventData AS ed NATURAL JOIN EnrolledDevice AS er NATURAL JOIN ServiceLocation AS sl NATURAL JOIN Address AS a JOIN EnergyPrice AS ep ON a.zip = ep.zip AND ed.event_time = ep.price_time 
        #                                     AND ed.event_time = ep.price_time
        #                                     WHERE event_type = 'Energy Use'
        #                                     GROUP BY LocationID;""").fetchall()
        # session["TCPL"] = total_cost_per_loc
        # total_cons_per_loc = cursor.execute("""SELECT LocationID, SUM(value)
        #                                     FROM EventData AS ed NATURAL JOIN EnrolledDevice NATURAL JOIN ServiceLocation AS sl
        #                                     WHERE ed.event_type = 'Energy Use'
        #                                     GROUP BY sl.LocationID""").fetchall()
        # connection.commit()
        # print(total_cons_per_loc)

        # 3 How your energy Cost Compares to Others
        # comparable_energy = cursor.execute("""WITH PerLocationEnergy AS (SELECT LocationID,SUM(CASE WHEN event_type = 'energy use' THEN value ELSE 0 END) AS TotalEnergy
        #                                    FROM ServiceLocation NATURAL JOIN EnrolledDevice NATURAL JOIN EventData 
        #                                    GROUP BY LocationID), AverageEnergyPerLocation AS (SELECT AVG(TotalEnergy) AS AvgEnergy, square_footage
        #                                    FROM PerLocationEnergy NATURAL JOIN ServiceLocation
        #                                    GROUP BY square_footage)
        #                                    SELECT ple.LocationID, ple.TotalEnergy / AVG(ae.AvgEnergy) * 100 AS PercentageOfAverage
        #                                    FROM PerLocationEnergy AS ple NATURAL JOIN ServiceLocation AS sl
        #                                    JOIN AverageEnergyPerLocation AS ae ON sl.square_footage BETWEEN ae.square_footage * 0.95 AND ae.square_footage * 1.05
        #                                    GROUP BY sl.LocationID;""").fetchall()
        # connection.commit()
        # session["compare"] = comparable_energy

        # 4 Most Expensive Hour Per Location
        # expense = cursor.execute("""SELECT EventID, MAX(value)
        #                          FROM EventData NATURAL JOIN DeviceModel NATURAL JOIN ServiceLocation
        #                          WHERE event_type = 'Energy Use'
        #                          GROUP BY LocationID""").fetchall()
        # connection.commit()
        # print(expense)

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
            next_address_id = get_next_Address_id()
            cursor.execute(
                'INSERT INTO Address (AddressID, address_type, unit, street, house_num, city, state, zip) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
                (next_address_id, 'location', unit, street, house_num, city, state, zip))
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
            model_id = request.form['model_id']
            model_type = request.form['model_type']
            model_number = request.form['model_number']
            other_details = request.form['other_details']

            next_device_id = get_next_DeviceID()
            cursor.execute(
                'INSERT INTO EnrolledDevice (DeviceID, LocationID, ModelID, d_hidden) VALUES (?, ?, ?, ?)',
                (next_device_id, location_id, model_id, 0),
            )
            connection.commit()
            cursor.execute(
                'INSERT INTO DeviceModel (ModelID, model_type, model_number, other_details) VALUES (?, ?, ?, ?)',
                (next_device_id, model_type, model_number, other_details)
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
