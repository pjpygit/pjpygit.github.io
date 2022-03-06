from flask import Flask, render_template, request, redirect, session, flash, jsonify, url_for

app = Flask(__name__)
app.secret_key = 'very secret many random bytes'


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run()
