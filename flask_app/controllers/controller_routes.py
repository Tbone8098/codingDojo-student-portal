from flask_app import app, bcrypt
from flask import render_template, redirect, request, session, flash, jsonify
from flask_app.config.utils import login_required
from flask_app.models import model_user

@app.route('/')
def index():
    if 'uuid' in session:
        return redirect('/dashboard')
    session['page'] = 'landing_page'
    return render_template('login.html')

@app.route('/dashboard')
@login_required
def dashboard():
    session['page'] = 'dashboard'
    return render_template('admin/dashboard.html')

@app.route('/register')
def register():
    return render_template('admin/register.html')

@app.route('/process/register', methods=['post'])
def process_register():
    if not model_user.User.validate_register(request.form):
        return redirect('/register')

    hash_pw = bcrypt.generate_password_hash(request.form['pw'])
    data = {
        **request.form,
        'pw': hash_pw,
        'level': 5
    }
    del data['confirm_pw']

    id = model_user.User.create(**data)
    session['uuid'] = id
    return redirect('/')

@app.route('/process/login', methods=['post'])
def process_login():
    if not model_user.User.validate_login(request.form):
        return redirect('/')
    
    if 'remember_me' in request.form:
        session['email'] = request.form['email']
    else:
        if 'email' in session:
            del session['email']
            
    return redirect('/dashboard')

@app.route('/logout')
def logout():
    del session['uuid']
    return redirect('/')

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return 'page not found'