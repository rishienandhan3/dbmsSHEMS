from flask import Flask
import sqlite3
import csv

app = Flask(__name__)

# Database connection function
def get_db_connection():
    connection = sqlite3.connect('shems.db')
    connection.row_factory = sqlite3.Row
    # cursor.execute('')
    return connection

connection = get_db_connection()
cursor = connection.cursor()


with open("utils/EnergyPrice.csv", newline='') as priceFile:
    price_reader = csv.reader(priceFile, delimiter = ",")
    for row in price_reader:
        # Insert into EnergyPrice Table
        cursor.execute("INSERT INTO EnergyPrice (price_time, zip, hourly_price) VALUES (?, ?, ?)", (row))
        connection.commit()

with open("utils/EventDataHourly.csv", newline='') as energyFile:
    energy_reader = csv.reader(energyFile, delimiter = ",")
    for row in energy_reader:
        cursor.execute("INSERT INTO EventData (EventID, DeviceID, event_type, label, value, event_time) VALUES (?, ?, ?, ?, ?, ?)", (row))
        connection.commit()


connection.close()

# if __name__ == '__main__':
#     app.run(debug=True)