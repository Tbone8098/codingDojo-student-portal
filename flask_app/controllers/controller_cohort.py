from flask_app import app
from flask import render_template, redirect, session, request

from flask_app.models import model_cohort

@app.route('/cohort/new')          
def cohort_new():
    return render_template('cohort_new.html')

@app.route('/cohort/create', methods=['POST'])          
def cohort_create():
    return redirect('/')

@app.route('/cohorts')          
def cohort_all():
    session['page'] = 'cohorts'
    return render_template('admin/cohort_all.html')

@app.route('/cohort/<int:id>')          
def cohort_show(id):
    return render_template('cohort_show.html')

@app.route('/cohort/<int:id>/edit')          
def cohort_edit(id):
    return render_template('cohort_edit.html')

@app.route('/cohort/<int:id>/update', methods=['POST'])          
def cohort_update(id):
    return redirect('/')

@app.route('/cohort/<int:id>/delete')          
def cohort_delete(id):
    return redirect('/')
