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
from flask_socketio import SocketIO
from app import app


socketio = SocketIO(app)

length=40
  
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
  
def allowed_file(filename):
 return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
 
def Generate(): #function generates a random 10 digit number
    randomstr = ''
    randomstr = ''.join(random.choices(string.ascii_letters+string.digits,k=length))
    return "pjoshi" + randomstr


@routes.route('/chat', methods=['GET', 'POST'])
def chat():
    return render_template('chat/index.html')
 
