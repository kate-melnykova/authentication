from collections import defaultdict
from datetime import datetime
from functools import wraps
import json
from logging import getLogger

from flask import Blueprint, render_template, request, url_for,\
    redirect, flash, make_response, current_app

from authentication.auth import crypting
from authentication.auth.models import User, AnonymousUser
from authentication.views.wtforms import LoginForm, RegistrationForm, UpdateUserForm
from authentication.models.exceptions import NotFound, ValidationError


def create_blueprint(redis=True, url=None):
    auth = Blueprint('auth', __name__, template_folder='templates')
    if url is not None:
        redis = True

    if redis and url is None:
        url = 'redis://redis:6379/0'
    return auth, redis, url
