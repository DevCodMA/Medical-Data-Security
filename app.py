from flask import Flask, request, render_template, jsonify, url_for
import sqlite3 as sql
import hashlib
import os
import warnings
import shutil

app = Flask(__name__)

hash = (lambda pswd: hashlib.sha256(pswd.encode('utf-8')).hexdigest())

check = False

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/home")
def home():
    if check:
        return render_template("home.html")
    else:
        return render_template('index.html')


@app.route("/login", methods=["POST"])
def login():
    global check
    uname = request.form["uname"]
    pswd = request.form["pswd"]

    conn = sql.connect("db/users.db")
    res = conn.execute(f"SELECT PSWD FROM USERS WHERE UNAME='{uname}'").fetchone()
    
    print(res)

    if hash(pswd) == res[0]:
        check = True
        return jsonify({'success': True, 'redirect': url_for('home')})
    else:
        return jsonify({'sucess': False})

@app.route("/register", methods=["POST"])
def register():
    uname = request.form["uname"]
    pswd = request.form["pswd"]
    fname = request.form["fname"]

    try:
        conn = sql.connect("db/users.db")
        cursor = conn.cursor()
        cursor.execute(f"INSERT INTO USERS VALUES ('{fname}', '{uname}', '{pswd}')")
        conn.commit()
        return "User registration successfull!"
    except Exception as ex:
        return f"User registration failed, error: {ex}"
    

@app.route("/logout")
def logout():
    global check
    check = False
    return jsonify({'success': True, 'redirect': url_for('home')})

    

@app.route("/process", methods=["POST"])
def process():
    return jsonify({})



if __name__ == '__main__':
    app.run(debug=True)