from flask import Flask, jsonify
from flask import request, abort
import datetime
import secrets
import json
import os

password = os.environ['password']

app = Flask(__name__)

tokens = {}

users = []


def saveUser():
    with open('workfile', 'w') as f:
        f.write(json.dumps(users))


def loadUser():
    global users

    user_string = None
    with open('workfile', 'r') as f:
        user_string = f.read()

    users = json.loads(user_string)


def auth(token):
    if token not in tokens:
        abort(401, description="Not authorized")


def usernames():
    out = []

    for u in users:
        out.append(u['name'])

    return out


@app.route('/getToken', methods=['POST'])
def getToken():
    if not request.json:
        abort(404, description="Resource not found")

    if request.json['pw'] == password:
        sec = secrets.token_bytes(32)
        tokens[sec] = datetime.datetime.now()
        return jsonify({'token': sec})


@app.route('/getUser', methods=['POST'])
def getUser():
    auth(request.json['pw'])

    return jsonify(usernames())


@app.route('/addUser', methods=['POST'])
def addUser():
    auth(request.json['pw'])
    name = request.json['name']
    cardID = None
    if name in usernames():
        users[name].append(cardID)
    else:
        users[name] = [cardID]
    return "OK"


@app.route('/removeUser', methods=['POST'])
def removeUser():
    auth(request.json['pw'])
    name = request.json['name']
    if name in usernames():
        del users[name]
        return "OK"
    else:
        abort(404)
    


if __name__ == '__main__':
    app.run(debug=True)
    loadUser()
