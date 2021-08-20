from flask import render_template, redirect, session, request
from . import routes
import requests


@routes.route('/order/<id>')
def order(id):
    if ('savedToken' in session.keys()):
        headers = {'x-auth-token': session['savedToken']}
        data = requests.get('http://localhost:5000/api/v1/orders/{}'.format(id), headers=headers)
        data = data.json()
        return render_template('order.html', data_one=data)
    return redirect('/')

@routes.route('/orders/ordersid/<ids>')
def allOrdersIds(ids):
    if ('savedToken' in session.keys()):
        headers = {'x-auth-token': session['savedToken']}
        data = requests.get('http://localhost:5000/api/v1/orders/ordersid/{}'.format(ids), headers=headers)
        data = data.json()
        return render_template('order.html', data_one=data)
    return redirect('/')