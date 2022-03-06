from flask import Flask, render_template, request, redirect, session, flash, jsonify, url_for

app = Flask(__name__)
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
