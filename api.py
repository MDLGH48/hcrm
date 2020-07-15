from flask import Flask, jsonify, request
from models import DataLayer, Student
import pandas as pd


app = Flask(__name__)


@app.route('/', methods=["GET"])
def index():
    return ("<h1 style='text-align:center'>welcome</h1>")


@app.route('/get_all', methods=['GET'])
def get_all():
    try:
        return jsonify(DataLayer().read_all_students())
    except Exception as e:
        return jsonify({"error": (str(e))})


@app.route('/get_students/<field>/<value>', methods=['GET'])
def get_students(field, value):
    try:
        return jsonify(DataLayer().filter_data(field, value))
    except Exception as e:
        return jsonify({"error": (str(e))})


@app.route('/cr_up/<action>', methods=['POST'])
def cr_up(action):
    try:
        if request.method == 'POST' and action == "create":
            req_data = request.get_json()
            DataLayer().create_student(req_data)
            return jsonify("Created")
    except Exception as e:
        return jsonify({"error": (str(e))})


if __name__ == "__main__":
    app.run()
