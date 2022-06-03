from flask_app import app
from flask_app.config.utils import login_required
from flask import render_template, redirect, session, request, jsonify

from flask_app.models import model_assignment

@app.route('/assignment/new')          
@login_required
def assignment_new():
    return render_template('assignment_new.html')

@app.route('/assignment/create', methods=['POST'])          
@login_required
def assignment_create():
    id = request.form['cohort_id']
    if not model_assignment.Assignment.validate(request.form):
        return redirect(f'/cohort/{id}/edit')

    model_assignment.Assignment.create(**request.form)
    return redirect(f'/cohort/{id}/edit')

@app.route('/assignment/bulk/<int:cohort_id>')
def assignment_bulk_add(cohort_id):
    context = {
        'cohort_id': cohort_id
    }
    return render_template('/admin/assignment_bulk.html', **context)

@app.route('/assignment/bulk/<int:cohort_id>/process', methods=['POST'])
def bulk_add(cohort_id):
    print(request.form)
    temp_list = []
    temp = ''
    for char in request.form['bulk']:
        if char.isalpha() or char.isdigit():
            temp += char
        else:
            if temp != '':
                temp_list.append(temp)
                temp = ''
    print(temp_list)
    return redirect(f'/cohort/{cohort_id}/edit')

@app.route('/assignment/<int:id>')          
@login_required
def assignment_show(id):
    return render_template('assignment_show.html')

@app.route('/assignment/<int:id>/edit')          
@login_required
def assignment_edit(id):
    return render_template('assignment_edit.html')

@app.route('/assignment/<int:id>/update', methods=['POST'])          
@login_required
def assignment_update(id):
    return redirect('/')

@app.route('/api/assignment/<int:id>/update', methods=['POST'])          
@login_required
def api_assignment_update(id):
    all_errors = {}

    input_dict = {
        'name': model_assignment.Assignment.validate_name_api, 
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
    model_assignment.Assignment.update_one(**request.form, id=id)
    res = {
        'status': 200
    }
    return jsonify(res)

@app.route('/assignment/<int:id>/delete/<int:cohort_id>')          
@login_required
def assignment_delete(id, cohort_id):
    model_assignment.Assignment.delete_one(id=id)
    return redirect(f'/cohort/{cohort_id}/edit')
