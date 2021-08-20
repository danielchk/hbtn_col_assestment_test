#!/usr/bin/python3
import jwt
import datetime
from flask import json, jsonify, request, abort
from app import mysql
from app.v1.views import app_views

def valid_token(encoded_jwt):
    try:
        payload = jwt.decode(encoded_jwt, "secret", algorithms=["HS256"])
        user_id = payload.get("id")
        query = "SELECT * FROM users WHERE id = %s"
        cur = mysql.connection.cursor()
        cur.execute(query, (user_id, ))
        data = cur.fetchall()
        
        if (data):
            return True
    except:
        return False


def getid_token(encoded_jwt):
    try:
        payload = jwt.decode(encoded_jwt, "secret", algorithms=["HS256"])
        user_id = payload.get("id")
        return user_id
    except:
        return None


def dict_order(order):
    return {
        "order_id": order[0],
        "order_date": order[1],
        "order_subtotal": '$' + str(order[2]),
        "order_taxes": '$' + str(order[3]),
        "order_total": '$' + str(order[4]),
        "order_status": "Paid" if order[5] == 1 else "Not paid",
        "gov_id": order[6],
        "customer_id": order[7],
        "company": order[8],
        "customer_name": order[9],
        "last_payment_date": order[10],
        "payment_type": order[11],
        "payment_status": order[12],
        "payment_txn_id": order[13],
        "payment_total": '$' + str(order[14]),
        "shipping_address": order[15],
        "shipping_city": order[16],
        "shipping_state": order[17],
        "shipping_country": order[18],
        "shipping_cost": '$' + str(order[19]),
    }

@app_views.route('/orders/<orders_id>', methods=['GET'], strict_slashes=False)
def get_order_by_id(orders_id):
    try:
        orders_by_id = []
        token = request.headers.get('x-auth-token')
        validToken = valid_token(token)
        
        if validToken:
            orders_id = orders_id.split(',')
            
            for order_id in orders_id:
                sql = "SELECT ord.id, ord.date, ord.subtotal, ord.taxes, \
                        ord.total, ord.paid, ord.gov_id, ord.user_id, \
                        u.company, CONCAT(u.name,' ',u.last_name), \
                        p.date, p.type, p.status, p.txn_id, p.total, \
                        s.address, s.city, s.state, s.country, s.cost \
                        FROM order AS ord \
                        INNER JOIN users AS u ON ord.user_id = u.id \
                        INNER JOIN payment AS p ON a.order_id = p.order_id \
                        INNER JOIN shipping AS s ON ord.order_id = s.order_id \
                        WHERE ord.id = %s"
                data = mysql_run(sql, (order_id,))
                
                for val in data:
                    order = dict_order(val)
                    orders_by_id.append(order)
            
            if len(orders_id) == 1:
                return jsonify(orders_by_id[0])
        else:
            return jsonify({"message": "Unauthorized"}), 401
        return jsonify(orders_by_id)
    except:
        return jsonify({"message": "Order not found"}), 404

@app_views.route('/orders/<date1>/<date2>', methods=['GET'],
                 strict_slashes=False)
def order_by_dates(date1, date2):
    try:
        order_by_dates = []
        token = request.headers.get('x-auth-token')
        validToken = valid_token(token)
        
        if validToken:
            query = "SELECT * from order WHERE date between %s AND %s"
            cursor = mysql.connection.cursor()
            cursor.execute(query, (date1, date2))
            data = cursor.fetchall()
            
            for val in data:
                order_by_dates.append(val)
            return jsonify(order_by_dates)
        else:
            return jsonify({"message": "Unauthorized"}), 401
    except:
        return jsonify({"message": "Orders not found"}), 404

@app_views.route('/orders/user_id/', methods=['GET'],
                 strict_slashes=False)
def orders_by_user_id(user_id):
    try:
        orders_by_userId = []
        token = request.headers.get('x-auth-token')
        validToken = valid_token(token)
        
        if validToken:
            user_id = getid_token(token)
            sql = "SELECT ord.id, ord.date, ord.subtotal, ord.taxes, \
                        ord.total, ord.paid, ord.gov_id, ord.user_id, \
                        u.company, CONCAT(u.name,' ',u.last_name), \
                        p.date, p.type, p.status, p.txn_id, p.total, \
                        s.address, s.city, s.state, s.country, s.cost \
                        FROM order AS ord \
                        INNER JOIN users AS u ON ord.user_id = u.id \
                        INNER JOIN payment AS p ON a.order_id = p.order_id \
                        INNER JOIN shipping AS s ON ord.order_id = s.order_id \
                        WHERE u.id = %s"
            data = mysql_run(sql, (user_id, ))
            
            for val in data:
                order = dict_order(val)
                orders_by_userId.append(order)
            return jsonify(orders_by_userId)
        else:
            return jsonify({"message": "you must be login"}), 401
    except:
        return jsonify({"message": "Orders not found"}), 404
