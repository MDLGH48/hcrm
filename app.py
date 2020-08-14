
import os
from flask import Flask, jsonify, request
from db import sign_up, login, create_data, get_data, update_data, delete_data
import pandas as pd


app = Flask(__name__)
port = int(os.environ.get("PORT", 5000))


def api_response(content):
    return jsonify({"data": content})


@app.route('/', methods=["GET"])
def index():
    return api_response("welcome")


@app.route('/login_user', methods=["POST"])
def login_user():
    req = request.get_json()
    user_name = req["user_name"]
    password = req["password"]
    return api_response(login(user_name, password))


@app.route('/create_user', methods=["POST"])
def create_user():
    req = request.get_json()
    user_name = req["user_name"]
    password = req["password"]
    email = req["email"]
    return api_response(sign_up(user_name, password, email))

# create


@app.route('/create_user_data', methods=["POST"])
def create_user_data():
    req = request.get_json()
    user_id = req["id"]
    data = req["data"]
    return api_response(create_data(user_id, data))

# read


@app.route('/get_user_data', methods=["GET"])
def get_user_data():
    req = request.get_json()
    user_id = req["id"]
    return api_response(get_data(user_id))

# update


@app.route('/update_user_data', methods=["PUT"])
def update_user_data():
    req = request.get_json()
    obj_id = req["id"]
    data = req["data"]
    return api_response(update_data(obj_id, data))

# delete


@app.route('/delete_user_data', methods=["DELETE"])
def delete_user_data():
    req = request.get_json()
    obj_id = req["id"]
    return api_response(delete_data(obj_id))


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=port)
