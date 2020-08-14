import os
import ssl
import pymongo
from bson.objectid import ObjectId


client = pymongo.MongoClient(
    os.getenv("MONGO_DB_URI"), ssl=True, ssl_cert_reqs=ssl.CERT_NONE)
crm_dev_db = client["crm_dev"]
user_collection = crm_dev_db["users"]
students_collection = crm_dev_db["students"]


def sign_up(user_name, password, email):
    user_collection.insert_one({
        "user": user_name,
        "password": password,
        "email": email})
    return {"message": "success",
            "id": str(user_collection.find_one({'user': user_name})["_id"])}


def login(user_name, password):
    find_user = user_collection.find_one({'user': user_name})
    if find_user == None:
        return {"message": "error", "error_type": "bad_user"}
    elif find_user["password"] != password:
        return {"message": "error", "error_type": "bad_password"}
    elif find_user["password"] == password:
        return {"message": "success", "id": str(find_user["_id"])}


def create_data(user_id, student_data):
    try:
        if type(student_data) is dict:
            student_data.update({"user_id": user_id})
            students_collection.insert_one(student_data)
            return {"message": {"success": student_data}}
        elif type(student_data) is list and all([type(student) is dict for student in student_data]):
            updated_user_students = [student.update(
                {"user_id": user_id}) for student in student_data]
            students_collection.insert_many(updated_user_students)
            return {"message": {"success": updated_user_students}}
        else:
            return {"message": student_data}
    except Exception as e:
        return {"error": str(e)}


def get_data(user_id, mode=None, key=None, val=None):
    students = list(students_collection.find({'user_id': user_id}))
    if mode == None:
        parsed_students = []
        for student in students:
            student.update({"student_id": str(student["_id"])})
            parsed_students.append(
                {key: student[key] for key in student.keys() - {'_id'}})
        return list(parsed_students)

    elif mode == "filter":
        filtered_students = list(students_collection.find(
            {'user_id': user_id, key: val}))
        parsed_filtered = []
        for student in filtered_students:
            student.update({"student_id": str(student["_id"])})
            parsed_filtered.append(
                {key: student[key] for key in student.keys() - {'_id'}})
        return parsed_filtered


def update_data(student_id, new_atts):
    students_collection.update_one(
        {"_id": ObjectId(student_id)}, {"$set": new_atts})
    return students_collection.find_one({"_id": ObjectId(student_id)})


def delete_data(student_id):
    try:
        students_collection.delete_one({"_id": ObjectId(student_id)})
        return {"success": "deleted"}
    except Exception as e:
        return {"error": str(e)}
