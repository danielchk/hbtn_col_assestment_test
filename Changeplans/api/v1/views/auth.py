#!/usr/bin/python3
from api.v1.views import app_views
from app import mysql
from flask import json, jsonify, request, abort
from flask_mysqldb import MySQL
import jwt


@app_views.route('/signup/', methods=['POST'], strict_slashes=False)
def signup():
    try:
        args = request.get_json()
        if args is None:
            return jsonify({"error": "Not a JSON"}), 400

        name = args.get("name")
        last_name = args.get("lastname")
        gov_id = args.get("govid")
        email = args.get("email")
        company = args.get("company")
        password = args.get("password")
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO users (name, last_name, gov_id, email, company, password) VALUES (%s, %s, %s, %s, %s, %s)',
                    (name, last_name, gov_id, email, company, password))
        return jsonify({"message": "User registered"})
    except:
        return jsonify({"message": "User already exists"}), 400


@app_views.route('/login/', methods=['POST'], strict_slashes=False)
def signin():
    try:
        args = request.get_json()
        email = args.get("email")
        password = args.get("password")
        sql = "SELECT * FROM users WHERE email = %s AND password = %s"
        cur = mysql.connection.cursor()
        cur.execute(sql, (email, password))
        userdata = cur.fetchall()
        if (not userdata):
            raise Exception

        user_id = userdata[0][0]
        encoded_jwt = jwt.encode({"id": user_id}, "secret", algorithm="HS256")
        return jsonify({"token": encoded_jwt})
    except TypeError err:
        return jsonify({"message": err})
    except:
        return jsonify({"message": "User does not exist"}), 404
