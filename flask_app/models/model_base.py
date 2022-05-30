from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app import DATABASE_SCHEMA
import re

class base_model:
    def __init__(self, data):
        self.id = data['id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.update = lambda **data : self.__class__.update(**data,id=self.id)
        self.delete = lambda **data : self.__class__.delete(**data,id=self.id)

    @classmethod
    def sanitize(self, paired=False, **data):
        col1 = []
        col2 = []
        for key in data:
            col1.append(f"`{key}`")
            col2.append(f"%({key})s")
        if paired:
            returnStr = ''
            for i in range(len(col1)):
                returnStr += f"{col1[i]} = {col2[i]}"
                if i != len(col1) - 1:
                    returnStr += ','
            return returnStr
        return ','.join(col1), ','.join(col2)

# C ************************************************

    @classmethod
    def create(cls, **data:dict):
        columns, values = cls.sanitize(**data)
        query = f'INSERT INTO {cls.table} ({columns}) VALUES ({values});'
        return connectToMySQL(DATABASE_SCHEMA).query_db(query, data)

# R ************************************************

    @classmethod
    def get_all(cls, where=False, where_clause=()):
        """
        If specifing a where clause then the where_clause variable is a tuple which needs two inputs. First is the category in which it needs to compare and second is the value that it should match. ie: "where {where_clause[0]} = {where_clause[1]}"
        """
        if not where:
            query = f'SELECT * FROM {cls.table}'
        else:
            query = f'SELECT * FROM {cls.table} WHERE {where_clause[0]} = {where_clause[1]}'
        results = connectToMySQL(DATABASE_SCHEMA).query_db(query)
        if results:
            all_table_name = []
            for table_name in results:
                all_table_name.append(cls(table_name))
            return all_table_name

    @classmethod
    def get_one(cls, **data):
        str = cls.sanitize(**data, paired=True)
        query = f'SELECT * FROM {cls.table} WHERE {str};'
        results = connectToMySQL(DATABASE_SCHEMA).query_db(query, data)
        if results:
           return cls(results[0])
        return results

# U ************************************************

    @classmethod
    def update_one(self, id, **data):
        str = self.sanitize(**data, paired=True)
        query = f'Update {self.table} SET {str} WHERE id = {id};'
        return connectToMySQL(DATABASE_SCHEMA).query_db(query,data)

# D ************************************************

    @classmethod   
    def delete_one(self, id, **data):
        str = self.sanitize(**data, paired=True)
        query = f'DELETE FROM {self.table} WHERE id = {id}'
        return connectToMySQL(DATABASE_SCHEMA).query_db(query,data)