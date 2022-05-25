from flask_app import app
from flask_app.config.utils import login_admin_required
from flask import render_template, redirect, session, request

from flask_app.models import model_student

@app.route('/student/new')          
@login_admin_required
def student_new():
    context = {}
    return render_template('student_new.html', **context)

@app.route('/student/create', methods=['POST'])          
@login_admin_required
def student_create():
    return redirect('/')

@app.route('/student/<int:id>')          
@login_admin_required
def student_show(id):
    context = {}
    return render_template('student_show.html', **context)

@app.route('/student/<int:id>/edit')          
@login_admin_required
def student_edit(id):
    context = {}
    return render_template('student_edit.html', **context)

@app.route('/student/<int:id>/update', methods=['POST'])          
@login_admin_required
def student_update(id):
    return redirect('/')

@app.route('/student/<int:id>/delete')          
@login_admin_required
def student_delete(id):
    return redirect('/')
