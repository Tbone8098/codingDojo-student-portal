from functools import wraps
from flask import request, redirect, session

def login_required(f):
    @wraps(f)
    def login(*args, **kwargs):
        if 'uuid' not in session:
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