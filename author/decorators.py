from functools import wraps
from flask import session, request, redirect, url_for, abort


def login_required(f):
    @wraps(f)
    #*args is positional parameters
    #**kwargs is named parameters
    def decorated_function(*args, **kwargs):
        # if not logged in then redirect to login page , 
        # and also pass calling page to return to after login
        if session.get('username') is None:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function
    
    
def author_required(f):
    @wraps(f)
    #*args is positional parameters
    #**kwargs is named parameters
    def decorated_function(*args, **kwargs):
        # if not logged in then redirect to login page , 
        # and also pass calling page to return to after login
        if session.get('is_author') is None:
            abort(403)
        return f(*args, **kwargs)
    return decorated_function
    
    
    
    