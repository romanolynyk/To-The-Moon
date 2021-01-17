from flask import render_template
from app import app


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/pltr')
def pltr():
    return render_template('pltr.html')

@app.route('/tsla')
def tsla():
    return render_template('tsla.html')

@app.route('/nio')
def nio():
    return render_template('nio.html')

