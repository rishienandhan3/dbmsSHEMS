from datetime import datetime
from flask import Flask
import sqlite3

app = Flask(__name__)

# Database connection function
def get_db_connection():
    connection = sqlite3.connect('shems.db')
    connection.row_factory = sqlite3.Row
    # cursor.execute('')
    return connection

connection = get_db_connection()
cursor = connection.cursor()


# Create Address Table
cursor.execute('''CREATE TABLE Address (
               AddressID INT(5) PRIMARY KEY,
               address_type VARCHAR(15) NOT NULL,
               unit VARCHAR(8) NOT NULL,
               street VARCHAR(30) NOT NULL,
               house_num INT(10) NOT NULL,
               city VARCHAR(30) NOT NULL,
               state VARCHAR(30) NOT NULL,
               zip VARCHAR(5) NOT NULL);''')
connection.commit()

# Insert data into Address Table
cursor.execute('''INSERT INTO Address (AddressID, address_type, unit, street, house_num, city, state, zip) 
               VALUES (1, 'billing', '377', 'Yun Fields', 22892, 'Schinnertown', 'OR', '14490');''')
connection.commit()

cursor.execute('''INSERT INTO Address (AddressID, address_type, unit, street, house_num, city, state, zip) 
               VALUES (2, 'service', '377', 'Yun Fields', 22892, 'Schinnertown', 'OR', '14490');''')
connection.commit()

cursor.execute('''INSERT INTO Address (AddressID, address_type, unit, street, house_num, city, state, zip) 
               VALUES (3, 'service', '576', 'Bibbert Rue', 721, 'Townshire', 'NV', '02992');''')
connection.commit()

cursor.execute('''INSERT INTO Address (AddressID, address_type, unit, street, house_num, city, state, zip) 
               VALUES (4, 'billing', '-1', 'Lesia Glen', 2983, 'Port Genaro', 'NM', '64033');''')
connection.commit()

cursor.execute('''INSERT INTO Address (AddressID, address_type, unit, street, house_num, city, state, zip) 
               VALUES (5, 'service', '542', 'Lesch Square', 5920, 'New Cheyenneview', 'LA', '06966');''')
connection.commit()


# Create User Table
cursor.execute('''CREATE TABLE User (
               UserID INT(5) PRIMARY KEY,
               first_name VARCHAR(50) NOT NULL,
               last_name VARCHAR(50) NOT NULL,
               email VARCHAR(100) NOT NULL,
               username VARCHAR(100) NOT NULL,
               password VARCHAR(100) NOT NULL,
               phone  VARCHAR(15) NOT NULL,
               AddressID INT(5) NOT NULL,
               FOREIGN KEY (AddressID) REFERENCES Address(AddressID));''')
connection.commit()


# Create ServiceLocation Table
cursor.execute('''CREATE TABLE ServiceLocation (
               LocationID INT(5) PRIMARY KEY,
               UserID INT(5) NOT NULL,
               AddressID INT(5) NOT NULL,
               move_in_date VARCHAR(50) NOT NULL,
               square_footage INT(10) NOT NULL,
               bedrooms INT(5) NOT NULL,
               occupants INT(5) NOT NULL,
               hidden BOOLEAN NOT NULL,
               FOREIGN KEY (UserID) REFERENCES User(UserID),
               FOREIGN KEY (AddressID) REFERENCES Address(AddressID));''')
connection.commit()

# Insert data into the ServiceLocation Table
cursor.execute("""INSERT INTO ServiceLocation (LocationID, UserID, AddressID, move_in_date, square_footage, bedrooms, occupants, hidden) 
               VALUES (1, 1, 2, '22/08/01 00:00:00', 4950, 3, 2, 0)""")
connection.commit()

cursor.execute('''INSERT INTO ServiceLocation (LocationID, UserID, AddressID, move_in_date, square_footage, bedrooms, occupants, hidden) 
               VALUES (2, 1, 3, '22/08/02 00:00:00', 5050, 4, 1, 0);''')
connection.commit()

cursor.execute('''INSERT INTO ServiceLocation (LocationID, UserID, AddressID, move_in_date, square_footage, bedrooms, occupants, hidden) 
               VALUES (3, 2, 5, '22/08/01 00:00:00', 5000, 5, 3, 0);''')
connection.commit()


# Create DeviceModel Table
cursor.execute('''CREATE TABLE DeviceModel (
               ModelID INT(5) PRIMARY KEY,
               model_type VARCHAR(20) NOT NULL,
               model_number VARCHAR(20) NOT NULL,
               other_details VARCHAR(200) NOT NULL);''')
connection.commit()

# Insert data into the DeviceModel Table
cursor.execute('''INSERT INTO DeviceModel (ModelID, model_type, model_number, other_details) 
               VALUES (1, 'Refrigerator', 'A2576', 'Energy Efficient');''')
connection.commit()

cursor.execute('''INSERT INTO DeviceModel (ModelID, model_type, model_number, other_details) 
               VALUES (2, 'Light Bulb', 'Q5008', 'Extra Bright');''')
connection.commit()

cursor.execute('''INSERT INTO DeviceModel (ModelID, model_type, model_number, other_details) 
               VALUES (3, 'Microwave', 'M270', 'None');''')
connection.commit()

cursor.execute('''INSERT INTO DeviceModel (ModelID, model_type, model_number, other_details) 
               VALUES (4, 'Air Conditioner', 'T4L23', '8000BTU');''')
connection.commit()

cursor.execute('''INSERT INTO DeviceModel (ModelID, model_type, model_number, other_details) 
               VALUES (5, 'Washing Machine', 'TL800', 'Extra Powerful');''')
connection.commit()


# Create the EnrolledDevice Table
cursor.execute('''CREATE TABLE EnrolledDevice (
               DeviceID INT(5) PRIMARY KEY,
               LocationID INT(5) NOT NULL,
               ModelID INT(5) NOT NULL,
               d_hidden BOOLEAN NOT NULL,
               FOREIGN KEY (LocationID) REFERENCES ServiceLocation(LocationID),
               FOREIGN KEY (ModelID) REFERENCES DeviceModel(ModelID));''')
connection.commit()

# Insert data into the EnrolledDevice Table
cursor.execute('''INSERT INTO EnrolledDevice (DeviceID, LocationID, ModelID, d_hidden) VALUES (1, 1, 1, 0);''')
connection.commit()

cursor.execute('''INSERT INTO EnrolledDevice (DeviceID, LocationID, ModelID, d_hidden) VALUES (2, 2, 1, 0);''')
connection.commit()

cursor.execute('''INSERT INTO EnrolledDevice (DeviceID, LocationID, ModelID, d_hidden) VALUES (3, 3, 1, 0);''')
connection.commit()

cursor.execute('''INSERT INTO EnrolledDevice (DeviceID, LocationID, ModelID, d_hidden) VALUES (4, 1, 3, 0);''')
connection.commit()

cursor.execute('''INSERT INTO EnrolledDevice (DeviceID, LocationID, ModelID, d_hidden) VALUES (5, 2, 3, 0);''')
connection.commit()

cursor.execute('''INSERT INTO EnrolledDevice (DeviceID, LocationID, ModelID, d_hidden) VALUES (6, 3, 3, 0);''')
connection.commit()

cursor.execute('''INSERT INTO EnrolledDevice (DeviceID, LocationID, ModelID, d_hidden) VALUES (7, 3, 3, 0);''')
connection.commit()

cursor.execute('''INSERT INTO EnrolledDevice (DeviceID, LocationID, ModelID, d_hidden) VALUES (8, 1, 4, 0);''')
connection.commit()

cursor.execute('''INSERT INTO EnrolledDevice (DeviceID, LocationID, ModelID, d_hidden) VALUES (9, 2, 4, 0);''')
connection.commit()

cursor.execute('''INSERT INTO EnrolledDevice (DeviceID, LocationID, ModelID, d_hidden) VALUES (10, 3, 4, 0);''')
connection.commit()

cursor.execute('''INSERT INTO EnrolledDevice (DeviceID, LocationID, ModelID, d_hidden) VALUES (11, 1, 5, 0);''')
connection.commit()

cursor.execute('''INSERT INTO EnrolledDevice (DeviceID, LocationID, ModelID, d_hidden) VALUES (12, 2, 5, 0);''')
connection.commit()

cursor.execute('''INSERT INTO EnrolledDevice (DeviceID, LocationID, ModelID, d_hidden) VALUES (13, 3, 5, 0);''')
connection.commit()

cursor.execute('''INSERT INTO EnrolledDevice (DeviceID, LocationID, ModelID, d_hidden) VALUES (14, 1, 2, 0);''')
connection.commit()

cursor.execute('''INSERT INTO EnrolledDevice (DeviceID, LocationID, ModelID, d_hidden) VALUES (15, 2, 2, 0);''')
connection.commit()

cursor.execute('''INSERT INTO EnrolledDevice (DeviceID, LocationID, ModelID, d_hidden) VALUES (16, 3, 2, 0);''')
connection.commit()

cursor.execute('''INSERT INTO EnrolledDevice (DeviceID, LocationID, ModelID, d_hidden) VALUES (17, 1, 2, 0);''')
connection.commit()

cursor.execute('''INSERT INTO EnrolledDevice (DeviceID, LocationID, ModelID, d_hidden) VALUES (18, 2, 2, 0);''')
connection.commit()

cursor.execute('''INSERT INTO EnrolledDevice (DeviceID, LocationID, ModelID, d_hidden) VALUES (19, 3, 2, 0);''')
connection.commit()


# Create the EventData Table
cursor.execute('''CREATE TABLE EventData (
               EventID INT(5) PRIMARY KEY,
               DeviceID INT(5) NOT NULL,
               event_type VARCHAR(15) NOT NULL,
               label VARCHAR(100) NOT NULL,
               value VARCHAR(30) NOT NULL,
               event_time VARCHAR(50) NOT NULL,
               FOREIGN KEY (DeviceID) REFERENCES EnrolledDevice(DeviceID));''')
connection.commit()

# Add data into the EventData Table
# new_datetime = datetime.strptime('22/08/01 00:00:00', '%y/%m/%d %H:%M:%S')
cursor.execute('''INSERT INTO EventData (EventID, DeviceID, event_type, label, value, event_time) 
               VALUES (1, 1, "Information", "Switched On", "0", '22/08/01 00:00:00');''')
connection.commit()

cursor.execute('''INSERT INTO EventData (EventID, DeviceID, event_type, label, value, event_time) 
               VALUES (2, 2, "Information", "Switched On", "0", '22/08/02 00:00:00');''')
connection.commit()

cursor.execute('''INSERT INTO EventData (EventID, DeviceID, event_type, label, value, event_time) 
               VALUES (3, 3, "Information", "Switched On", "0", '22/08/01 00:00:00');''')
connection.commit()

cursor.execute('''INSERT INTO EventData (EventID, DeviceID, event_type, label, value, event_time) 
               VALUES (4, 4, "Information", "Switched On", "0", '22/08/01 00:00:00');''')
connection.commit()

cursor.execute('''INSERT INTO EventData (EventID, DeviceID, event_type, label, value, event_time) 
               VALUES (5, 5, "Information", "Switched On", "0", '22/08/02 00:00:00');''')
connection.commit()

cursor.execute('''INSERT INTO EventData (EventID, DeviceID, event_type, label, value, event_time) 
               VALUES (6, 6, "Information", "Switched On", "0", '22/08/01 00:00:00');''')
connection.commit()

cursor.execute('''INSERT INTO EventData (EventID, DeviceID, event_type, label, value, event_time) 
               VALUES (7, 7, "Information", "Switched On", "0", '22/08/01 00:00:00');''')
connection.commit()

cursor.execute('''INSERT INTO EventData (EventID, DeviceID, event_type, label, value, event_time) 
               VALUES (8, 8, "Information", "Switched On", "0", '22/08/01 00:00:00');''')
connection.commit()

cursor.execute('''INSERT INTO EventData (EventID, DeviceID, event_type, label, value, event_time) 
               VALUES (9, 9, "Information", "Switched On", "0", '22/08/02 00:00:00');''')
connection.commit()

cursor.execute('''INSERT INTO EventData (EventID, DeviceID, event_type, label, value, event_time) 
               VALUES (10, 10, "Information", "Switched On", "0", '22/08/01 00:00:00');''')
connection.commit()

cursor.execute('''INSERT INTO EventData (EventID, DeviceID, event_type, label, value, event_time) 
               VALUES (11, 11, "Information", "Switched On", "0", '22/08/01 00:00:00');''')
connection.commit()

cursor.execute('''INSERT INTO EventData (EventID, DeviceID, event_type, label, value, event_time) 
               VALUES (12, 12, "Information", "Switched On", "0", '22/08/02 00:00:00');''')
connection.commit()

cursor.execute('''INSERT INTO EventData (EventID, DeviceID, event_type, label, value, event_time) 
               VALUES (13, 13, "Information", "Switched On", "0", '22/08/01 00:00:00');''')
connection.commit()

cursor.execute('''INSERT INTO EventData (EventID, DeviceID, event_type, label, value, event_time) 
               VALUES (14, 14, "Information", "Switched On", "0", '22/08/01 00:00:00');''')
connection.commit()

cursor.execute('''INSERT INTO EventData (EventID, DeviceID, event_type, label, value, event_time) 
               VALUES (15, 15, "Information", "Switched On", "0", '22/08/02 00:00:00');''')
connection.commit()

cursor.execute('''INSERT INTO EventData (EventID, DeviceID, event_type, label, value, event_time) 
               VALUES (16, 16, "Information", "Switched On", "0", '22/08/01 00:00:00');''')
connection.commit()

cursor.execute('''INSERT INTO EventData (EventID, DeviceID, event_type, label, value, event_time) 
               VALUES (17, 17, "Information", "Switched On", "0", '22/08/01 00:00:00');''')
connection.commit()

cursor.execute('''INSERT INTO EventData (EventID, DeviceID, event_type, label, value, event_time) 
               VALUES (18, 18, "Information", "Switched On", "0", '22/08/02 00:00:00');''')
connection.commit()

cursor.execute('''INSERT INTO EventData (EventID, DeviceID, event_type, label, value, event_time) 
               VALUES (19, 19, "Information", "Switched On", "0", '22/08/01 00:00:00');''')
connection.commit()

cursor.execute('''INSERT INTO EventData (EventID, DeviceID, event_type, label, value, event_time) 
               VALUES (20, 1, "Information", "Refrigerator Door Open", "0", '22/08/05 14:02:07');''')
connection.commit()

cursor.execute('''INSERT INTO EventData (EventID, DeviceID, event_type, label, value, event_time) 
               VALUES (21, 1, "Information", "Refrigerator Door Close", "0", '22/08/05 14:20:54');''')
connection.commit()

cursor.execute('''INSERT INTO EventData (EventID, DeviceID, event_type, label, value, event_time) 
               VALUES (22, 2, "Information", "Refrigerator Door Open", "0", '22/08/06 09:00:05');''')
connection.commit()

cursor.execute('''INSERT INTO EventData (EventID, DeviceID, event_type, label, value, event_time) 
               VALUES (23, 2, "Information", "Refrigerator Door Close", "0", '22/08/06 09:30:26');''')
connection.commit()

cursor.execute('''INSERT INTO EventData (EventID, DeviceID, event_type, label, value, event_time) 
               VALUES (24, 3, "Information", "Refrigerator Door Open", "0", '22/08/10 16:24:00');''')
connection.commit()

cursor.execute('''INSERT INTO EventData (EventID, DeviceID, event_type, label, value, event_time) 
               VALUES (25, 3, "Information", "Refrigerator Door Close", "0", '22/08/10 16:34:00');''')
connection.commit()


# Create the EventData Table
cursor.execute('''CREATE TABLE EnergyPrice (
               price_time VARCHAR(50) NOT NULL,
               zip VARCHAR(5) NOT NULL,
               hourly_price FLOAT(6) NOT NULL,
               PRIMARY KEY (price_time, zip));''')
connection.commit()

connection.close()

# if __name__ == '__main__':
#     app.run(debug=True)