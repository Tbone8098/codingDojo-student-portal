from flask_app import app
from flask import render_template, redirect, session, request
from flask_app.config.utils import check_logged_in_id, login_required

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
@app.route('/settings/<subpage>')     
@login_required 
def user_edit(subpage='user'):
    session['page'] = 'settings'

    context = {
        'user': model_user.User.get_one(id=session['uuid']),
        'subpage' : subpage
    }

    if session['level'] >= 5:
        return render_template('user_edit.html', **context)
    return render_template('user_edit.html')

@app.route('/user/<int:id>/update', methods=['POST'])          
@login_required
@check_logged_in_id
def user_update(id):
    data = {
        **request.form
    }
    model_user.User.update_one(**data, id=id)
    return redirect('/')

@app.route('/user/<int:id>/delete')          
def user_delete(id):
    return redirect('/')
