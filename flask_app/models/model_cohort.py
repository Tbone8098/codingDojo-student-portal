from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import model_base, model_stack
from flask_app import DATABASE_SCHEMA
from datetime import datetime

class Cohort(model_base.base_model):
    table = 'Cohorts'
    def __init__(self, data):
        super().__init__(data)
        self.start_date = data['start_date']
        self.end_date = data['end_date']
        self.stack_id = data['stack_id']
        self.creator_id = data['creator_id']
        self.is_current = data['is_current']

    @property
    def current_stack(self):
        return model_stack.Stack.get_one(id=self.stack_id)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM cohorts JOIN stacks ON cohorts.stack_id = stacks.id;"
        results = connectToMySQL(DATABASE_SCHEMA).query_db(query)
        if results:
            all_cohorts = []
            for dict in results:
                cohort = cls(dict)
                data = {
                    **dict,
                    'id': dict['stacks.id'],
                    'created_at': dict['stacks.created_at'],
                    'updated_at': dict['stacks.updated_at'],
                }
                cohort.stack = model_stack.Stack(data)
                all_cohorts.append(cohort)
            return all_cohorts
        return []


    @staticmethod
    def validate(data:dict) -> bool:
        is_valid = True
        
        if len(data['stack_id']) < 1:
            is_valid = False
            flash('field is required', 'err_cohort_type')
        
        if len(data['start_date']) < 1:
            is_valid = False
            flash('field is required', 'err_cohort_start_date')
        
        if len(data['end_date']) < 1:
            is_valid = False
            flash('field is required', 'err_cohort_end_date')

        return is_valid
