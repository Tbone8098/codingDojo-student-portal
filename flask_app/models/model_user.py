from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, session
from flask_app.models import model_base
from flask_app import bcrypt
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class User(model_base.base_model):
    table = 'Users'
    def __init__(self, data):
        super().__init__(data) 
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.pw = data['pw']
        self.level = data['level']

    @staticmethod
    def validate_login(data:dict) -> bool:
        is_valid = True

        if len(data['email']) < 1:
            is_valid = False
            flash('Email is required', 'err_user_email_login')
        elif not EMAIL_REGEX.match(data['email']): 
            flash("Invalid email address!", 'err_user_email_login')
            is_valid = False
        else:
            potential_user = User.get_one(email= data['email'])
            if not potential_user:
                flash("Invalid Credentials", 'err_user_email_login')
                is_valid = False

        if len(data['pw']) < 1:
            is_valid = False
            flash('Password is required', 'err_user_pw_login')
        
        if is_valid:
            if not bcrypt.check_password_hash(potential_user.pw, data['pw']):
                is_valid = False
                flash("Invalid Credentials", 'err_user_email_login')
            else:
                session['uuid'] = potential_user.id
                session['level'] = potential_user.level

        return is_valid

    @staticmethod
    def validate_register(data:dict) -> bool:
        is_valid = True

        if len(data['name']) < 1:
            is_valid = False
            flash('name is required', 'err_user_name_login')

        if len(data['email']) < 1:
            is_valid = False
            flash('Email is required', 'err_user_email_login')
        elif not EMAIL_REGEX.match(data['email']): 
            flash("Invalid email address!", 'err_user_email_login')
            is_valid = False
        else:
            potential_user = User.get_one(email= data['email'])
            if potential_user:
                flash("Email already in use", 'err_user_email_login')
                is_valid = False

        if len(data['pw']) < 1:
            is_valid = False
            flash('Password is required', 'err_user_pw_login')

        if len(data['confirm_pw']) < 1:
            is_valid = False
            flash('Confirm Password is required', 'err_user_confirm_pw_login')

        return is_valid