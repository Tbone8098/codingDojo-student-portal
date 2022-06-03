import json
from flask_app import app, bcrypt
from flask_app.config.utils import login_required, login_admin_required, generate_rndm
from flask import render_template, redirect, session, request, jsonify
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

from flask_app.models import model_student, model_user, model_assignment, model_students_have_assignments, model_cohort_has_students

@app.route('/student/request_password/<int:user_id>')
def request_password(user_id):
    code = generate_rndm()
    model_user.User.update_one(id = user_id, temp_code = code)
    return redirect(f'/student/codingdojo/{code}')

@app.route('/student/codingdojo/<code>')          
def student_initLogin(code):
    user = model_user.User.get_one(temp_code=code)
    if user:
        context = {
            'user': user
        }
        return render_template('basic_user/student_register.html', **context)
    return redirect('/')

@app.route('/student/<int:user_id>/reset_password', methods=['post'])
def student_reset_password(user_id):
    hash_pw = bcrypt.generate_password_hash(request.form['pw'])
    model_user.User.update_one(id=user_id, pw=hash_pw, temp_code='')
    session['uuid'] = user_id
    session['level'] = 1
    return redirect('/')

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
        'nickname': request.form['name']
    }

    student_id = model_student.Student.create(**data)

    records = model_cohort_has_students.CohortHasStudent.get_all(where=True, where_clause=('student_id', student_id))
    if records:
        for record in records:
            model_cohort_has_students.CohortHasStudent.update_one(id = record.id, is_active=0)
    model_cohort_has_students.CohortHasStudent.create(student_id=student_id, cohort_id=cohort_id, is_active=1)

    # add 
    assignments = model_assignment.Assignment.get_all({'cohort_id': cohort_id})
    for assignment in assignments:
        model_students_have_assignments.StudentsHasAssignments.create(student_id=student_id,assignment_id=assignment.id)

    return redirect(f'/cohort/{cohort_id}/edit')

@app.route('/student/bulk_add/<int:cohort_id>')
def student_bulk_add(cohort_id):
    context = {
        'cohort_id': cohort_id
    }
    return render_template('admin/student_bulk.html', **context)

@app.route('/student/bulk_process', methods=['post'])
def student_bulk_process():
    print(request.form)
    cohort_id = request.form['cohort_id']
    
    temp_list = []
    temp = ''
    for char in request.form['bulk']:
        if char.isalpha() or char == '@' or char.isdigit() or char == '.':
            temp += char
        elif EMAIL_REGEX.match(temp):
            email = temp
            name = ' '.join(temp_list[0:])
            potential_user = model_user.User.get_one(email=temp)
            if potential_user:
                pass
            else:
                url = generate_rndm()
                user_id = model_user.User.create(email=email, name=name, temp_code=url)
                student_id = model_student.Student.create(user_id=user_id, nickname=name)
                model_cohort_has_students.CohortHasStudent.create(student_id=student_id, cohort_id=cohort_id)
            temp = ''
            temp_list = []
        else:
            if temp != '':
                temp_list.append(temp)
                temp = ''

    return redirect(f'/cohort/{cohort_id}/edit')

@app.route('/student/<int:id>/login')          
@login_admin_required
def student_login(id):
    student = model_student.Student.get_one(id=id)
    
    session['uuid'] = student.user.id
    session['level'] = student.user.level
    return redirect('/')

@app.route('/student/all')
def all_students():
    context = {
        'all_students': model_student.Student.get_all_join_users()
    }
    return render_template('admin/student_all.html', **context)

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

@app.route('/api/student/mass/delete', methods=['POST'])          
@login_required
def student_mass_delete():
    print(request.form['list'])
    list = json.loads(request.form['list'])
    for item in list:
        cohort = model_cohort_has_students.CohortHasStudent.get_one(student_id = item['student_id'])
        model_cohort_has_students.CohortHasStudent.delete_one(id = cohort.id)
        model_student.Student.delete_one(id=item['student_id'])
        model_user.User.delete_one(id=item['user_id'])
    return jsonify(msg='success')

@app.route('/profile')
@app.route('/profile/<subpage>')
@login_required
def student_profile(subpage='user'):
    context = {
        'subpage': subpage,
        'student': model_student.Student.get_one(user_id=session['uuid']),
        'user': model_user.User.get_one(id=session['uuid']),
    }
    return render_template("basic_user/profile.html", **context)

@app.route("/leaderboard")
def leader_board():
    return render_template("basic_user/leaderboard.html")

@app.route("/calendar")
def calendar():
    return render_template("basic_user/calendar.html")