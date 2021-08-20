#!/usr/bin/python3
from flask import json, jsonify, request, abort
from app import mysql
from api.v1.views import app_views
import jwt


def valid_token(encoded_jwt):
    try:
        payload = jwt.decode(encoded_jwt, "secret", algorithms=["HS256"])
        user_id = payload.get("id")
        sql = "SELECT * FROM users WHERE user_id = %s"
        cur = mysql.connection.cursor()
        cur.execute(sql, (user_id, ))
        data = cur.fetchall()
        if (not data):
            raise Exception
        return True
    except:
        return False


def dict_user(user):
    return {
        "name": user[1],
        "last_name": user[2],
        "email": user[3],
        "gov_id": user[4],
        "company": user[5],
    }


@app_views.route('/users/all', methods=['GET'], strict_slashes=False)
def get_all_users():
    try:
        users = []
        token = request.headers.get('x-auth-token')
        validToken = valid_token(token)
        if validToken:
            cur = mysql.connection.cursor()
            query = "SELECT * FROM users"
            cur.execute(query)
            data = cur.fetchall()
            for val in data:
                user = dict_user(val)
                users.append(user)
            return jsonify(users)
        else:
            return jsonify({"message": "You are not loggin"}), 401
    except:
        return jsonify({"message": "A problem searching for Users"})
