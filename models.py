import os
import datetime
import json
import requests


class DataLayer:

    def __student_file_loc(self):
        return "data/students.json"

    def read_all_students(self):
        with open(self.__student_file_loc(), "r") as student_file_read:
            student_list = json.loads(student_file_read.read())
        student_file_read.close()
        return student_list

    def update_all_students(self, updated_content):
        with open(self.__student_file_loc(), "w") as student_file_write:
            student_file_write.write(json.dumps(updated_content))
        student_file_write.close()

    def create_student(self, student):
        student_list = self.read_all_students()
        student_list.append(student)
        self.update_all_students(student_list)

    def del_student(self, field, value):
        student_list = self.read_all_students()
        student_list.remove(
            [student for student in student_list if student[field] == value])
        self.update_all_students(student_list)

    def filter_data(self, key, val):
        student_list = self.read_all_students()
        return [item for item in student_list if item[key] == val]


class Student(DataLayer):
    def __init__(self, ID, f_name, l_name, email, password, created_at, updated, skill, skill_level, d_skill, d_skill_level):
        super().__init__()
        self.ID = ID
        self.f_name = f_name
        self.l_name = l_name
        self.email = email
        self.password = password
        self.created_at = str(datetime.datetime.now())
        self.updated = ""
        self.skill = skill
        self.skill_level = skill_level
        self.d_skill = d_skill
        self.d_skill_level = d_skill_level

    @property
    def updated(self):
        return self.updated

    @updated.setter
    def updated(self):
        self.updated = str(datetime.datetime.now())
        # self.update_all_students(content)
