from flask_app import app
from flask import render_template, redirect, session, request, jsonify
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
def user_update(id):
    model_user.User.update_one(**request.form, id=id)
    return redirect('/')

@app.route('/api/user/<int:id>/update', methods=['POST'])          
@login_required
def api_user_update(id):
    all_errors = {}

    input_dict = {
        'name': model_user.User.validate_name_api, 
        'email': model_user.User.validate_email_api, 
        'pw': model_user.User.validate_pw_api
        }

    for item in input_dict:
        if item in request.form:
            errors = input_dict[item](request.form)
            if len(errors) > 0:
                for key in errors:
                    all_errors[key] = errors[key]

    print(all_errors)
    if len(all_errors):
        res = {
            'status': 404,
            'errors': all_errors
        }
        return jsonify(res)
    model_user.User.update_one(**request.form, id=id)
    res = {
        'status': 200
    }
    return jsonify(res)


@app.route('/user/<int:id>/delete')          
def user_delete(id):
    return redirect('/')

