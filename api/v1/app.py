#!/usr/bin/python3
"""flask Run, MySQL"""
from os import environ
from flask import Flask, make_response, jsonify
from flask_mysqldb import MySQL
from api.v1.views import app_views

app = Flask(__name__)
app.register_blueprint(app_views)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'retailer'

mysql = MySQL(app)

@app.errorhandler(404)
def not_found(error):
    """ Function if error happens(404)"""
    return make_response(jsonify({'error': "Not found"}), 404)

if __name__ == "__main__":
    """Run in port"""
    app.run(host='0.0.0.0', port='5000', threaded=True, debug=True)
