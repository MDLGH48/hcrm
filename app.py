import os
from flask import Flask, jsonify, request, make_response
import jwt
import datetime
from db import sign_up, login, create_data, get_data, update_data, delete_data
import pandas as pd
from auth import token_required, validate_user

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")


@app.route('/', methods=["GET"])
def index():
    return make_response(jsonify('welcome'), 200)


@app.route('/login_user', methods=["POST"])
def login_user():
    auth = request.authorization
    check_user = login(auth.username, auth.password)
    if check_user["authenticated"]:
        token = jwt.encode({'user_id': check_user["user_id"], 'exp': datetime.datetime.utcnow(
        ) + datetime.timedelta(days=2)}, app.config['SECRET_KEY'], algorithm='HS256')
        return jsonify({'token': token.decode('UTF-8')})
    return make_response(jsonify({"message": 'login failed'}), 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})


@app.route('/signup', methods=["POST"])
def signup():
    try:
        request_body = request.get_json()
        user_name = request_body["user_name"]
        password = request_body["password"]
        email = request_body["email"]
        user_validate = validate_user(user_name, password, email)
        if user_validate == True:
            new_user = sign_up(user_name, password, email)
            token = jwt.encode({'user': new_user, 'exp': datetime.datetime.utcnow(
            ) + datetime.timedelta(days=2)}, app.config['SECRET_KEY'], 'HS256')
            return jsonify({'token': token.decode('UTF-8')})
        else:
            return make_response(jsonify({"message": user_validate}), 409)
    except KeyError:
        return make_response(jsonify({"message": "missing fields"}), 409)


@app.route('/jwt_test', methods=["POST"])
@token_required
def jwt_test():
    token = jwt.decode(
        request.headers.get('token')[1:-1], app.config['SECRET_KEY'], algorithms='HS256')
    return jsonify(token)
# create


@app.route('/create_user_data', methods=["POST"])
@token_required
def create_user_data():
    user_id = jwt.decode(
        request.headers.get('token')[1:-1], app.config['SECRET_KEY'], algorithms='HS256')["user"]
    request_body = request.get_json()
    data = request_body["data"]
    return jsonify(create_data(user_id, data))

# read


@app.route('/get_user_data', methods=["GET"])
@token_required
def get_user_data():
    user_id = jwt.decode(
        request.headers.get('token')[1:-1], app.config['SECRET_KEY'], algorithms='HS256')["user"]
    return jsonify(get_data(user_id))

# update


@app.route('/update_user_data', methods=["PUT"])
@token_required
def update_user_data():
    user_id = jwt.decode(
        request.headers.get('token')[1:-1], app.config['SECRET_KEY'], algorithms='HS256')["user"]
    request_body = request.get_json()
    data = request_body["data"]
    return jsonify(update_data(user_id, data))

# delete


@app.route('/delete_user_data', methods=["DELETE"])
@token_required
def delete_user_data():
    request_body = request.get_json()
    return jsonify(delete_data(request_body["student_id"]))


port = int(os.environ.get("PORT", 5000))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=port)
