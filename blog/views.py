from flask_blog import app
from flask import render_template, redirect
from author.form import RegisterForm

@app.route('/')
@app.route('/index')
def index():
    return "hello world!"
    
