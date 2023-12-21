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





connection.close()

if __name__ == '__main__':
    app.run(debug=True)