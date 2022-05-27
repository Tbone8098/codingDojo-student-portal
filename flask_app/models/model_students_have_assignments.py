from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import model_base, model_user
from flask_app import DATABASE_SCHEMA
import re

class students_has_assignments(model_base.base_model):
    table = 'students_has_assignments'
    def __init__(self, data):
        super().__init__(data)
        self.assignment_id = data['assignment_id']
        self.student_id = data['student_id']
        self.is_completed = data['is_completed']