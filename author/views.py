from flask_blog import app
from flask import render_template, redirect, url_for, session, request, flash
from author.form import RegisterForm, LoginForm
from author.models import Author
from author.decorators import login_required
import bcrypt

@app.route('/login', methods=('GET', 'POST'))
def login():
    #return "Hello, User!"
    form = LoginForm()
    error = None
    
    if request.method == 'GET' and request.args.get('next'):
        session['next'] = request.args.get('next',None)
        
        
    if form.validate_on_submit():
        #return redirect(url_for('loggedin'))
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(form.password.data, salt)
#        author = Author.query.filter_by(
#            username = form.username.data,
#            password = form.password.data
#            ).limit(1)
# changed for hashed password
        author = Author.query.filter_by( 
            username = form.username.data
            ).first()
            

            
        if author:
            # bcrypt form data using salt from database password, if they match then ok
            if bcrypt.hashpw(form.password.data, author.password) == author.password:
                
                session['username'] = form.username.data
                session['is_author'] = author.is_author
                #flash("user %s" % form.username.data )
                flash("user %s " % form.username.data)
                if 'next' in session:
                    next = session.get('next')
                    session.pop('next')
                    return redirect(next)
                else: 
                    return redirect(url_for('index'))
            else:
                error = "Incorrect username and password1"
        else:
            error = "Incorrect username and password2"
    return render_template('author/login.html', form=form, error=error)
    

@app.route('/register', methods=('GET', 'POST'))
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        return redirect(url_for('success'))
    return render_template('author/register.html', form=form)

@app.route('/success')
def success():
    return "Author Registered!"
    
@app.route('/login_success')
@login_required
def login_success():
    return "Author Logged In"
    
@app.route('/loggedin')
def loggedin():
    return "Author LoggedIn!"    
    
    
@app.route('/logout')
def logout():
    #flash("logged out")
    session.pop('username')
    session.pop('is_author')
    return redirect('index')
