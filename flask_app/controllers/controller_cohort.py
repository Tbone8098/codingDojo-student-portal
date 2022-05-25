from flask_app import app
from flask import render_template, redirect, session, request, flash
from flask_app.config.utils import check_logged_in_id,login_admin_required

from flask_app.models import model_cohort, model_stack

@app.route('/cohort/new')
@login_admin_required           
def cohort_new():
    session['page'] = 'cohort_new'
    context = {
        'all_stacks': model_stack.Stack.get_all(),
    }
    return render_template('admin/cohort_new.html', **context)

@app.route('/cohort/create', methods=['POST'])
@login_admin_required           
def cohort_create():
    if not model_cohort.Cohort.validate(request.form):
        return redirect('/cohort/new')

    model_cohort.Cohort.create(**request.form, creator_id=session['uuid'])
    return redirect('/cohorts')

@app.route('/cohorts')
@login_admin_required            
def cohort_all():
    session['page'] = 'cohorts'
    context = {
        'all_cohorts': model_cohort.Cohort.get_all()
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
    }
    return render_template('admin/cohort_edit.html', **context)

@app.route('/cohort/<int:id>/update', methods=['POST'])
@login_admin_required           
def cohort_update(id):
    print(request.form)
    model_cohort.Cohort.update_one(id=id, **request.form)
    return redirect('/cohorts')

@app.route('/cohort/<int:id>/delete')
@login_admin_required    
def cohort_delete(id):
    cohort = model_cohort.Cohort.get_one(id=id)
    if session['uuid'] != cohort.creator_id:
        flash("You can't do that!" , 'err_notifications')
        return redirect('/cohorts')
    model_cohort.Cohort.delete_one(id=id)
    return redirect('/cohorts')
