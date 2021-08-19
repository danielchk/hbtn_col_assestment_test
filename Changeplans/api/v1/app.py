#!/usr/bin/python3
"""
Flask Application
"""
from flask import Flask, make_response, jsonify
from flask_mysqldb import MySQL
from os import environ

app = Flask(__name__)
from api.v1.views import app_views
app.register_blueprint(app_views)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'retailer'

mysql = MySQL(app)

@app.errorhandler(404)
def not_found(error):
    """ 404 Not Found"""
    return make_response(jsonify({'error': "Not found"}), 404)

if __name__ == "__main__":
    """
    Main funtion
    """
    app.run(host='0.0.0.0', port='5000', threaded=True, debug=True)
