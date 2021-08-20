"""import blueprints and run flask"""
from flask import Flask, Blueprint
from routes import auth, orders

app = Flask(__name__)

app.register_blueprint(routes)

if __name__ == '__main__':
    app.secret_key = '1qazxsw2"#3edc*)'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(port=6000, threaded=True, debug=True)  #Set port
