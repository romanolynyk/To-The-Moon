from flask import render_template
from app import app
from test import line
from htn_postprocessing import tohtml

@app.route('/')
@app.route('/index')
def index():
    #tohtml()
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

