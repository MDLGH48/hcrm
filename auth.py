import os
import re
import dns.resolver
from functools import wraps
import datetime
import jwt
from flask import Flask, request, jsonify
from db import user_collection


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('token')[1:-1]
        print(token)
        if not token:
            return jsonify({'message': 'Token is missing!'}), 403
        try:
            jwt.decode(token, os.getenv("SECRET_KEY"), 'HS256')
        except:
            return jsonify({'message': 'Token is invalid!'}), 403

        return f(*args, **kwargs)

    return decorated


def password_format(password, length):
    is_good_length = len(password) >= length
    has_special_chars = re.search(re.compile(
        '[@_!`#$%^&*()<>?/\|}{~:]'), password) != None
    is_alpha_num_caps_and_lower = re.search(
        re.compile('[a-zA-Z0-9]'), password) != None
    has_no_white_space = re.search(' ', password) == None
    return is_good_length and has_special_chars and is_alpha_num_caps_and_lower and has_no_white_space


def email_valid(email):
    if re.match(r"[^@]+@[^@]+\.[^@]+", email) == None:
        return False
    else:
        try:
            dns.resolver.resolve(email.rsplit('@', 1)[-1], 'MX')
            return True
        except dns.resolver.NoAnswer:
            return False


def validate_user(user_name, password, email, length=8):
    if user_name.isalnum() == False:
        return "user name must contain alpha numeric characters"
    if password_format(password, length) == False:
        return f"password must must be at least {length} characters long \
            with at least one upper and one lower case letter, \
            at least one special character and no white spaces"
    if email_valid(email) == False:
        return "email address does not exist"
    if user_collection.find_one({'user': user_name}) != None:
        return "user name taken"
    else:
        return True
