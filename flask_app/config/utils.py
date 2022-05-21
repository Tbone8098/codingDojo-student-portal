from functools import wraps
from flask import request, redirect, session

def login_required(f):
    @wraps(f)
    def login(*args, **kwargs):
        if 'uuid' not in session:
            return redirect('/')
        return f(*args, **kwargs)
    return login