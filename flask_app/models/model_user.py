from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import model_base
from flask_app import DATABASE_SCHEMA
import re

class User(model_base.base_model):
    table = 'Users'
    def __init__(self, data):
        super().__init__(data) 
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.pw = data['pw']

    @staticmethod
    def validate_login(data:dict) -> bool:
        is_valid = True

        if len(data['email']) < 1:
            is_valid = False
            flash('Email is required', 'err_user_email_login')

        if len(data['pw']) < 1:
            is_valid = False
            flash('Password is required', 'err_user_pw_login')

        return is_valid