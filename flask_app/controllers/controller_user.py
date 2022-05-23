from flask_app import app
from flask import render_template, redirect, session, request
from flask_app.config.utils import login_required

from flask_app.models import model_user

@app.route('/user/new')          
def user_new():
    model_user.User.something()
    return render_template('user_new.html')

@app.route('/user/create', methods=['POST'])          
def user_create():
    return redirect('/')

@app.route('/user/<int:id>')          
def user_show(id):
    return render_template('user_show.html')

@app.route('/settings')     
@login_required 
def user_edit():
    session['page'] = 'settings'

    context = {
        'user': model_user.User.get_one(id=session['uuid'])
    }

    if session['level'] >= 5:
        return render_template('admin/user_edit.html', **context)
    return render_template('user_edit.html')

@app.route('/user/<int:id>/update', methods=['POST'])          
def user_update(id):
    return redirect('/')

@app.route('/user/<int:id>/delete')          
def user_delete(id):
    return redirect('/')
