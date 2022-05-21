from cmath import log
from pyexpat import model
from flask_app import app
from flask import render_template, redirect, request, session, flash, jsonify
from flask_app.config.utils import login_required
from flask_app.models import model_user

@app.route('/')
def index():
    session['page'] = 'landing_page'
    return render_template('login.html')

@app.route('/dashboard')
@login_required
def dashboard():
    session['page'] = 'dashboard'
    return render_template('admin/dashboard.html')

@app.route('/process/login', methods=['post'])
def process_login():
    if not model_user.User.validate_login(request.form):
        return redirect('/')
    return redirect('/dashboard')

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return 'page not found'