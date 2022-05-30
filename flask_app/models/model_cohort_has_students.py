from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import model_base, model_student
from flask_app import DATABASE_SCHEMA

class CohortHasStudent(model_base.base_model):
    table = 'Cohort_has_students'
    def __init__(self, data):
        super().__init__(data)
        self.cohort_id = data['cohort_id']
        self.student_id = data['student_id']
        self.is_active = data['is_active']
    
    @property
    def student(self):
        return model_student.Student.get_one(id=self.student_id)