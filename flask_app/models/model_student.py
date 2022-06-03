from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import model_base, model_user, model_students_have_assignments
from flask_app import DATABASE_SCHEMA


class Student(model_base.base_model):
    table = 'Students'
    def __init__(self, data):
        super().__init__(data)
        self.nickname = data['nickname']
        self.need_to_contact = data['need_to_contact']
        self.ap_status = data['ap_status']
        self.ap_options = ['none', 'On AP', 'Complete']
        self.ap_count = data['ap_count']
        self.sessions_missed = data['sessions_missed']
        self.lpacp = data['lpacp']
        self.user_id = data['user_id']
        self.exam_status = data['exam_status']
        self.exam_options = ['Red', 'Black', 'Fail', 'Inpro', 'none']

    @property
    def user(self):
        return model_user.User.get_one(id=self.user_id)
    
    @property 
    def assignments(self):
        query = f"SELECT * FROM students_has_assignments JOIN assignments ON assignments.id = students_has_assignments.assignment_id WHERE students_has_assignments.student_id = {self.id};"
        results = connectToMySQL(DATABASE_SCHEMA).query_db(query)
        if results:
            all_assignments = []
            for dict in results:
                all_assignments.append(model_students_have_assignments.students_has_assignments(dict))
            return all_assignments
        return []

    @property
    def core_count(self):
        assignments = self.assignments
        count = 0
        for assignment in assignments:
            if assignment.is_completed:
                count += 1
        return count

    # @classmethod
    # def get_all(cls, **data) -> list:
    #     query = "SELECT * FROM students WHERE cohort_id = %(cohort_id)s"
    #     results = connectToMySQL(DATABASE_SCHEMA).query_db(query, data)
    #     if results:
    #         all_students = []
    #         for dict in results:
    #             all_students.append(cls(dict))
    #         return all_students
    #     return []

    @classmethod
    def get_all_join_users(cls):
        query = "SELECT * FROM students JOIN users ON users.id = students.user_id;"
        results = connectToMySQL(DATABASE_SCHEMA).query_db(query)
        if results:
            all_students = []
            for dict in results:
                student = cls(dict)
                data = {
                    **dict,
                    'id': dict['users.id'],
                    'created_at': dict['users.created_at'],
                    'updated_at': dict['users.updated_at'],
                }
                student.user_info = model_user.User(data)
                all_students.append(student)
            return all_students
        return []

    @staticmethod
    def validate(data:dict) -> bool:
        is_valid = True

        if len(data['name']) < 1:
            is_valid = False
            flash('field is required', 'err_student_name')
        
        return is_valid

    
    @staticmethod
    def validate_nickname_api(data:dict) -> dict:
        errors = {}

        if len(data['nickname']) < 1:
            errors['err_user_nickname'] = 'nickname is required'

        return errors