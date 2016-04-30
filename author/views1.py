from flask_blog import app
from flask import render_template, redirect
from author.form import RegisterForm


@app.route('/login')
def login():
    return " hello user"
    
@app.route('/register', methods=['GET','POST'])
def register():
    #import pdb; pdb.set_trace()
    
    form = RegisterForm()
    return render_template('author/register.html', form=form)
    


