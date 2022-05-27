from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import model_base, model_user
from flask_app import DATABASE_SCHEMA
import re

class Assignment(model_base.base_model):
    table = 'Assignments'
    def __init__(self, data):
        super().__init__(data)
        self.name = data['name']
        self.week = data['week']

    @classmethod
    def get_all(cls, data:dict) -> bool:
        query = "SELECT * FROM assignments WHERE cohort_id = %(cohort_id)s"
        results = connectToMySQL(DATABASE_SCHEMA).query_db(query,data)
        if results:
            all_assignments = []
            for dict in results:
                all_assignments.append(cls(dict))
            return all_assignments
        return []


    @staticmethod
    def validate(data:dict) -> bool:
        is_valid = True

        if len(data['name']) < 1:
            is_valid = False
            flash('Name is required', 'err_assignment_name')

        if len(data['week']) < 1:
            is_valid = False
            flash('week is required', 'err_assignment_week')

        return is_valid