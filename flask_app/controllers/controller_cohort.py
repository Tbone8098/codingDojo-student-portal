from flask_app import app
from flask import render_template, redirect, session, request, flash, jsonify
from flask_app.config.utils import check_logged_in_id,login_admin_required

from flask_app.models import model_cohort, model_stack, model_cohort_has_students, model_assignment

@app.route('/cohort/new')
@login_admin_required           
def cohort_new():
    session['page'] = 'cohort_new'
    test = model_stack.Stack.get_all()
    print(test)
    # check stacks
    if not model_stack.Stack.get_all():
        stack_list = ['python', 'MERN', 'C#', 'Java']
        for item in stack_list:
            model_stack.Stack.create(name=item)

    context = {
        'all_stacks': model_stack.Stack.get_all(),
    }
    return render_template('admin/cohort_new.html', **context)

@app.route('/cohort/create', methods=['POST'])
@login_admin_required           
def cohort_create():
    if not model_cohort.Cohort.validate(request.form):
        return redirect('/cohort/new')

    id = model_cohort.Cohort.create(**request.form, creator_id=session['uuid'])
    return redirect(f'/cohort/{id}/edit')

@app.route('/cohort/all')
@login_admin_required            
def cohort_all():
    print(request.args)
    approved_columns = ['is_current', 'stack_id', 'start_date', 'end_date']
    approved_orders = ['desc', 'asc']
    
    data = {'column': 'is_current', 'order': 'asc'}

    if request.args.get('column') in approved_columns:
        print("test A")
        print(request.args.get('column'))
        data['column'] = request.args.get('column')

    if request.args.get('order') in approved_orders:
        print("test B")
        print(request.args.get('order'))
        data['order'] = request.args.get('order')

    print(data)

    context = {
        'all_cohorts': model_cohort.Cohort.get_all(data)
    }
    return render_template('admin/cohort_all.html', **context)

@app.route('/cohort/<int:id>')
@login_admin_required          
def cohort_show(id):
    return render_template('cohort_show.html')

@app.route('/cohort/<int:id>/edit')    
@login_admin_required      
def cohort_edit(id):
    context = {
        'cohort': model_cohort.Cohort.get_one(id=id),
        'all_stacks': model_stack.Stack.get_all(),
        'all_students': model_cohort_has_students.CohortHasStudent.get_all(where=True, where_clause=('cohort_id', id)),
        'all_assignments': model_assignment.Assignment.get_all({'cohort_id':id})
    }
    return render_template('admin/cohort_edit.html', **context)

@app.route('/cohort/<int:id>/update', methods=['POST'])
@login_admin_required           
def cohort_update(id):
    print(request.form)
    model_cohort.Cohort.update_one(id=id, **request.form)
    return redirect('/cohorts')

@app.route('/api/cohort/<int:id>/update', methods=['post'])
@login_admin_required
def api_cohort_update(id):
    model_cohort.Cohort.update_one(id=id, **request.form)
    return jsonify(msg="success")

@app.route('/cohort/<int:id>/delete')
@login_admin_required    
def cohort_delete(id):
    cohort = model_cohort.Cohort.get_one(id=id)
    if session['uuid'] != cohort.creator_id:
        flash("You can't do that!" , 'err_notifications')
        return redirect('/cohorts')
    model_cohort.Cohort.delete_one(id=id)
    return redirect('/cohort/all')
