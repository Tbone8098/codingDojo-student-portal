from flask_app import app, bcrypt
from flask_app.config.utils import login_required, login_admin_required
from flask import render_template, redirect, session, request, jsonify

from flask_app.models import model_student, model_user

# @app.route('/student/new')          
# @login_required
# def student_new():
#     context = {}
#     return render_template('student_new.html', **context)

@app.route('/student/create', methods=['POST'])          
@login_admin_required
def student_create():
    cohort_id = request.form['cohort_id']
    if not model_student.Student.validate(request.form):
        return redirect(f'/cohort/{cohort_id}/edit')

    data = {
        **request.form,
        'pw': bcrypt.generate_password_hash(request.form['name'])
    }
    del data['cohort_id']
    user_id = model_user.User.create(**data)

    data = {
        'user_id': user_id,
        'cohort_id': cohort_id,
        'nickname': request.form['name']
    }

    model_student.Student.create(**data)
    return redirect(f'/cohort/{cohort_id}/edit')

@app.route('/student/bulk_add')
def bulk_add():
    return render_template('admin/student_bulk.html')

@app.route('/student/<int:id>/login')          
@login_admin_required
def student_login(id):
    student = model_student.Student.get_one(id=id)
    
    session['uuid'] = student.user.id
    session['level'] = student.user.level
    return redirect('/')

@app.route('/student/<int:id>/edit')          
@login_admin_required
def student_edit(id):
    context = {
        'student': model_student.Student.get_one(id=id),
    }
    return render_template('admin/student_edit.html', **context)

@app.route('/student/<int:id>/update', methods=['POST'])          
@login_required
def student_update(id):
    return redirect('/')

@app.route('/api/student/<int:id>/update', methods=['POST'])          
@login_required
def api_student_update(id):
    all_errors = {}

    input_dict = {
        'nickname': model_student.Student.validate_nickname_api, 
        }

    for item in input_dict:
        if item in request.form:
            errors = input_dict[item](request.form)
            if len(errors) > 0:
                for key in errors:
                    all_errors[key] = errors[key]

    if len(all_errors):
        res = {
            'status': 404,
            'errors': all_errors
        }
        return jsonify(res)
    model_student.Student.update_one(**request.form, id=id)
    res = {
        'status': 200
    }
    return jsonify(res)

@app.route('/student/<int:id>/delete')          
@login_required
def student_delete(id):
    return redirect('/')

@app.route('/student/<int:id>/<int:cohort_id>/remove')          
@login_required
def student_remove(id, cohort_id):
    model_student.Student.update_one(cohort_id=None, id=id)
    return redirect(f'/cohort/{cohort_id}/edit')


@app.route('/profile')
@app.route('/profile/<subpage>')
@login_required
def student_profile(subpage='user'):
    context = {
        'subpage': subpage
    }
    return render_template("basic_user/profile.html", **context)

@app.route("/leaderboard")
def leader_board():
    return render_template("basic_user/leaderboard.html")

@app.route("/calendar")
def calendar():
    return render_template("basic_user/calendar.html")