from flask import Flask, jsonify, request
from models import DataLayer, Student
import pandas as pd
from flask_restplus import Resource, Api


app = Flask(__name__)
api = Api(app, version='1.0', title='Hogwarts API',
          description='Hogwarts students CRM').namespace("Students", description="")


@api.route('/get_all')
class GetAll(Resource):
    def get(self):
        return {"students": DataLayer().read_all_students()}


@api.route('/get_students/<field>/<value>')
@api.doc(params={'field': 'the field to query a student by', 'value': 'the value of the desired field'})
class GetOne(Resource):
    def get(self, field, value):
        return {"student": jsonify(DataLayer().filter_data(field, value))}


@api.route('/create')
@api.doc(params={"student": "all fields needed to create student"})
class Create(Resource):
    def post(self):
        req_data = request.get_json()
        return {"new_student": DataLayer().create_student(req_data)}


@api.route('/delete/<field>/<value>')
@api.doc(params={'field': 'the field to delete a student by', 'value': 'the value of the desired field'})
class Delete(Resource):
    def delete(self, field, value):
        return {"Deleted": DataLayer().del_student(field, value)}


if __name__ == "__main__":
    app.run()
