from flask import Flask, render_template, request, redirect, session, flash, jsonify, url_for, Blueprint
from functools import wraps
import re
from werkzeug.utils import secure_filename
import os
from datetime import datetime
import sqlite3
from . import routes
import random
import string

length=40
  
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
  
def allowed_file(filename):
 return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
 
def Generate(): #function generates a random 10 digit number
    randomstr = ''
    randomstr = ''.join(random.choices(string.ascii_letters+string.digits,k=length))
    return "pjoshi" + randomstr






 
@routes.route('/signup', methods=['GET', 'POST'])
def signup():
    msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'name' in request.form and 'password' in request.form and 'email' in request.form:
        # Create variables for easy access
        name = request.form['name']
        email = request.form['email']
        contact = request.form['contact']
        password = request.form['password']
        full_name = request.form['full_name']
        date = request.form['date']
        address = request.form['address']
        file = request.files['file']
        # Check if account exists using MySQL
        con = sqlite3.connect("clinic.db")
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute('SELECT * FROM user WHERE name = ?', (name,))
        account = cur.fetchone()
        # If account exists show error and validation checks
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', name):
            msg = 'Username must contain only characters and numbers!'
        elif not name or not password or not email:
            msg = 'Please fill out the form!'
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            newfilename = Generate()+filename
            file.save(os.path.join('/static/uploads', newfilename))
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            cur.execute('INSERT INTO user VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, ?)', (name, email, contact, password, full_name, date, address, newfilename))
            con.commit()
            msg = 'You have successfully registered!'
            return render_template('index.html', msg=msg)
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show registration form with message (if any)
    
    return render_template('index.html', msg=msg)



@routes.route('/login', methods=['POST', 'GET'])
def login():

    status = True
    if request.method == 'POST':
        name = request.form["name"]
        password = request.form["password"]
        con = sqlite3.connect("clinic.db")
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("select * from user where name=? and password=?", (name, password))
        data = cur.fetchone()
        if data:
            session['logged_in'] = True
            session['username'] = data["name"]
            session['id'] = data["id"]
            session['email'] = data["email"]
            flash('Login Successfully', 'success')
            return redirect('profile')
        else:
            flash('Invalid Login. Try Again', 'danger')
    return render_template("index.html")

# check if user logged in
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please Login', 'danger')
            return redirect(url_for('login'))

    return wrap


@routes.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('routes.login'))


@routes.route('/profile')
def profile():
    if 'logged_in' in session:
        con = sqlite3.connect("clinic.db")
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("select * from user WHERE name = ?", (session['username'],))
        rows = cur.fetchall()
        return render_template("profile.html", rows=rows)
    else:
        return redirect(url_for('routes.login'))



if __name__ == '__main__':
    app.run()
