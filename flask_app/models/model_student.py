from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import model_base, model_user
from flask_app import DATABASE_SCHEMA
import re

class Student(model_base.base_model):
    table = 'Students'
    def __init__(self, data):
        super().__init__(data)
        self.nickname = data['nickname']
        self.current_cohort_id = data['current_cohort_id']
        self.need_to_contact = data['need_to_contact']
        self.ap_status = data['ap_status']
        self.ap_count = data['ap_count']
        self.sessions_missed = data['sessions_missed']
        self.lpacp = data['lpacp']
        self.user_id = data['user_id']