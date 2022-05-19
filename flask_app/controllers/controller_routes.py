from flask_app import app
from flask import render_template, redirect, request, session, flash, jsonify
from flask_app.models import model_user

@app.route('/')
def index():
    if 'uuid' in session:
        return redirect('/dashboard')
    session['page'] = 'landing_page'
    return render_template('onlooker/index.html')

@app.route('/dashboard')
def dashboard():
    if 'uuid' not in session:
        return redirect('/')
    session['page'] = 'dashboard'
    return render_template('admin/dashboard.html')

@app.route('/login')
def login():
    return render_template('admin/login.html')

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return 'page not found'