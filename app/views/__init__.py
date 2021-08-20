#!/usr/bin/python3
"""Blueprint"""
from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/app/v1')

from app.v1.views.auth import *
from app.v1.views.orders import *
from app.v1.views.users import *
