from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import model_base, model_assignment
from flask_app import DATABASE_SCHEMA
import re

class StudentsHasAssignments(model_base.base_model):
    table = 'students_has_assignments'
    def __init__(self, data):
        super().__init__(data)
        self.assignment_id = data['assignment_id']
        self.student_id = data['student_id']
        self.is_completed = data['is_completed']

    @property
    def info(self):
        query = f'SELECT * FROM assignments JOIN students_has_assignments ON students_has_assignments.assignment_id = assignments.id WHERE students_has_assignments.assignment_id = {self.assignment_id}'
        result = connectToMySQL(DATABASE_SCHEMA).query_db(query)
        if result:
            return model_assignment.Assignment(result[0])