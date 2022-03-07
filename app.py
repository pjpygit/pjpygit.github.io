from flask import Flask, render_template, request, redirect, session, flash, jsonify, url_for
from functools import wraps
import re
from werkzeug.utils import secure_filename
import os
from datetime import datetime
import sqlite3
import random, threading, webbrowser
from routes import *
from waitress import serve
from sqlite3 import Error


app = Flask(__name__)
app.register_blueprint(routes)
app.secret_key = 'very secret many random bytes'



@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/login_p')
def login_p():
    return render_template('login_p.html')

@app.route('/reg_p')
def reg_p():
    return render_template('reg_p.html')


if __name__ == "__main__":
    app.run()
