from flask import Flask, request, jsonify
import pymongo
import json
from bson import json_util

app = Flask(__name__)

client = pymongo.MongoClient('localhost', 27017)
db = client.testdb


@app.route('/getdetails', methods=['GET'])
def GetDetails():
    json_docs = []
    for doc in db.PersonalInfo.find():
        json_doc = json.dumps(doc, default=json_util.default)
        json_docs.append(json_doc)
    return jsonify(json_docs)

@app.route('/adddetails', methods=['POST'])
def AddDetails():
    user = request.get_json()
    if db.PersonalInfo.find_one({"email": user['email']}):
        return jsonify('Email already in use'), 400
    db.PersonalInfo.insert_one(user)
    return jsonify(True), 200

@app.route('/deletedetails', methods=['DELETE'])
def DeleteDetails():
    email = request.args.get('email')
    print(email)
    if db.PersonalInfo.find_one({"email": email}):
        db.PersonalInfo.delete_one({"email": email})
        return jsonify(True), 200
    else:
        return jsonify('Invalid email'), 400

@app.route('/updatename', methods=['PUT'])
def UpdateName():
    user = request.get_json()
    print(user)
    if db.PersonalInfo.find_one({"email": user['email']}):
        db.PersonalInfo.update_one({"email": user['email']},
        {'$set':{'name': user['name']}})
        return jsonify(True), 200
    else:
        return jsonify('Invalid email'), 400