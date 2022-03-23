from flask import Flask, render_template, request, redirect, session, flash, jsonify, url_for, Blueprint
from flask_socketio import SocketIO, emit, join_room, leave_room
from functools import wraps
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
from werkzeug.utils import secure_filename
import os
from datetime import datetime
import random
import string
from engineio.payload import Payload
import json
from flask_cors import CORS, cross_origin

# Next two lines are for the issue: https://github.com/miguelgrinberg/python-engineio/issues/142
from engineio.payload import Payload







Payload.max_decode_packets = 2


length=40


ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
  
def allowed_file(filename):
 return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
 
def Generate(): #function generates a random 10 digit number
    randomstr = ''
    randomstr = ''.join(random.choices(string.ascii_letters+string.digits,k=length))
    return "pjoshi" + randomstr

app = Flask(__name__)


app.secret_key = 'your secret key'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'online_consulting'

mysql = MySQL(app)
socketio = SocketIO(app)



UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER  




_users_in_room = {} # stores room wise user list
_room_of_sid = {} # stores room joined by an used
_name_of_sid = {} # stores display name of users






@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/success')
def success():
    return render_template('success.html')

@app.route('/users')
def users():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM profile')
    rows = cursor.fetchall()
    return render_template('users.html', rows=rows)


@app.route('/login', methods =['GET', 'POST'])
def login():
	msg = ''
	if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
		username = request.form['username']
		password = request.form['password']
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM user WHERE username = % s AND password = % s', (username, password, ))
		account = cursor.fetchone()
		if account:
			session['loggedin'] = True
			session['id'] = account['id']
			session['username'] = account['username']
			msg = 'Logged in successfully !'
			return redirect(url_for('profile', id = session['id']))
		else:
			msg = 'Incorrect Username or Password !'
	return render_template('index.html', msg = msg)

@app.route('/logout')
def logout():
	session.pop('loggedin', None)
	session.pop('id', None)
	session.pop('username', None)
	return redirect(url_for('login'))







@app.route('/profile_compl/<id>', methods =['GET', 'POST'])
def profile_compl(id):
        
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user WHERE id = %s', (id, ))
        account = cursor.fetchall()
        
        return render_template('complete_profile.html', account = account, id = account[0])

@app.route('/complete_profile', methods =['GET', 'POST'])
def complete_profile():
    msgpr = ''
    if request.method == 'POST':
        
        
        id = request.form['id']
        fullname = request.form['fullname']
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        age = request.form['age']
        gender = request.form['gender']
        contact = request.form['contact']
        address = request.form['address']
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            newfilename = Generate()+filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], newfilename))
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('INSERT INTO profile VALUES (% s, % s, % s, % s, % s, % s, % s, % s, % s, % s)', (id, fullname, username, password, email, age, gender, contact, address, newfilename, ))
            mysql.connection.commit()
            msgpr = 'You have successfully create profile !'
    return render_template('index.html', msgpr = msgpr)
    
    
    
    
@app.route('/profile/<id>', methods =['GET', 'POST'])
def profile(id):
        
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM profile WHERE id = %s', (id, ))
        users = cursor.fetchall()
        
        return render_template('profile.html', users = users)
    
    
    
    
    
    
    
    

@app.route('/register', methods =['GET', 'POST'])
def register():
    msg = ''
    msge = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form :
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user WHERE username = % s', (username, ))
        account = cursor.fetchone()
        cursor.execute('SELECT * FROM user WHERE email = % s', (email, ))
        emailchk = cursor.fetchone()
        if account:
            msg = 'Username already exists !'
        elif emailchk:
            msge = 'Email already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers !'
        elif not username or not password or not email:
            msg = 'Please fill out the form !'
        else:
            cursor.execute('INSERT INTO user VALUES (NULL, % s, % s, % s)', (username, password, email, ))
            mysql.connection.commit()
            msg = 'You have successfully registered !'
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('register.html', msg = msg, msge = msge)    
    
    
    






@app.route("/video_call/<id>", methods=["GET", "POST"])
def video_call(id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM profile WHERE id = %s', (session['id'], ))
    users = cursor.fetchall()
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM profile')
    otherUser = cursor.fetchall()
    
    return render_template("/video_call.html", users = users, otherUser = otherUser)
   


if __name__ == "__main__":
    app.run()











