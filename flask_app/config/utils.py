from functools import wraps
from flask import request, redirect, session, flash

def login_required(f):
    @wraps(f)
    def login(*args, **kwargs):
        if 'uuid' not in session:
            flash('You need to be logged in!', 'err_notifications')
            return redirect('/')
        return f(*args, **kwargs)
    return login

def login_admin_required(f):
    @wraps(f)
    def login(*args, **kwargs):
        if 'uuid' not in session or session['level'] < 5:
            flash('You are not admin!', 'err_notifications')
            return redirect('/')
        return f(*args, **kwargs)
    return login

def check_logged_in_id(f):
    @wraps(f)
    def check(*args, **kwargs):
        if session['uuid'] != kwargs['id']:
            return redirect('/')
        return f(*args, **kwargs)
    return check

def history(data:dict):
    if 'history' not in session:
        session['history']
    
    print(data)