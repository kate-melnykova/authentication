from collections import defaultdict
from datetime import datetime
from functools import wraps
import json
from logging import getLogger

from flask import Blueprint, render_template, request, url_for,\
    redirect, flash, make_response, current_app


def init_auth_blueprint(redis_url=''):
    auth = Blueprint('auth', __name__, template_folder='templates')
    if not redis_url:
        redis_url = current_app.config.get('REDIS_URL', 'redis://redis:6379/0')
    with open('config.py', 'a+') as config:
        config.write(f'REDIS_URL={redis_url}')
    return auth



