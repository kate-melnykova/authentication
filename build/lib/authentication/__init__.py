from collections import defaultdict
from datetime import datetime
from functools import wraps
import json
from logging import getLogger

from flask import Blueprint, render_template, request, url_for,\
    redirect, flash, make_response

from authentication.auth import crypting
from authentication.auth.models import User, AnonymousUser
from authentication.views.wtforms import LoginForm, RegistrationForm, UpdateUserForm
from authentication.models.exceptions import NotFound, ValidationError

__all__ = ['User', 'AnonymousUser', 'NotFound', 'ValidationError', 'auth', 'login_required']

auth = Blueprint('auth', __name__, template_folder='templates')
logger = getLogger(__name__)


@auth.before_request
def get_current_user():
    encrypted_username = request.cookies.get('username')
    if encrypted_username is None:
        request.user = AnonymousUser()
    else:
        try:
            username = crypting.aes_decrypt(encrypted_username)
        except UnicodeDecodeError:
            request.user = AnonymousUser()
        else:
            try:
                request.user = User.load(username)
            except NotFound:
                request.user = AnonymousUser()


def login_required(func):
    @wraps(func)
    def wrapped(*args, **kwargs):
        if not request.user.is_authenticated():
            r = make_response(redirect(url_for('login')))
            r.delete_cookie('username')
            r.delete_cookie('first_name')
            flash('You are not logged in')
            return r
        else:
            return func(*args, **kwargs)

    return wrapped


@auth.context_processor
def inject_user():
    return dict(user=request.user)


@auth.route('/login')
def login():
    form_error = request.cookies.get('form_error')
    try:
        form_error = json.load(form_error)
    except TypeError:
        form_error = defaultdict(str)
    except AttributeError:
        form_error = defaultdict(str)
    if not request.user.is_authenticated():
        login_form = LoginForm(request.form)
        return render_template('login.html', loginform=login_form)
    return redirect(url_for('logout'))


@auth.route('/login/processing', methods=["POST"])
def login_processing():
    if request.user.is_authenticated():
        flash('You are already logged in!')
        return redirect(url_for('hello_world'))

    loginform = LoginForm(request.form)
    if loginform.validate():
        username = loginform.username.data
        password = loginform.password.data
        r = make_response(redirect(url_for('hello_world')))
        try:
            user = User.load(username)
        except NotFound:
            logger.info(f'user {username} is not found')
            r = make_response(redirect(url_for('login')))
            flash("Incorrect credentials: please double-check username")
            return r

        logger.info(f'Login: user password is {user.password}')
        logger.info(f'Login: password entered is {password}')
        if user.verify_password(password):
            encrypted_username = crypting.aes_encrypt(username)
            if loginform.rememberme.data:
                r.set_cookie('username', encrypted_username,
                             expires=datetime.datetime.now() + datetime.timedelta(days=365))
                r.set_cookie('first_name', user.first_name,
                             expires=datetime.datetime.now() + datetime.timedelta(days=365))

            else:
                r.set_cookie('username', encrypted_username)
                r.set_cookie('first_name', user.first_name)
            flash('You are successfully logged in!')
            return r
        else:
            flash("Incorrect credentials: please double-check username and password")
            r.set_cookie('form_error', json.dumps(loginform.errors))
            return redirect(url_for('login'))


@auth.route('/logout')
@login_required
def logout():
    return render_template('logout.html')


@auth.route('/logout/confirmed', methods=["POST"])
@login_required
def logout_process():
    r = make_response(redirect(url_for('login')))
    r.delete_cookie('username')
    r.delete_cookie('first_name')
    flash('Successfully logged out')
    return r


@auth.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.user.is_authenticated():
        flash('You are already logged in!')
        return redirect(url_for('welcome'))

    if request.method == 'GET':
        regform = RegistrationForm()
        r = make_response(render_template('registration.html', regform=regform))
        return r


@auth.route('/registration/processing', methods=["POST"])
def registration_processing():
    form = RegistrationForm(request.form)
    if not form.validate():
        flash('Error: incorrect entry in the form')
        r = make_response(redirect(url_for('registration')))
        r.set_cookie('form_error', json.dumps(form.errors))
        return r

    username = form.username.data
    if not User.exists(username):
        password = form.password.data
        first_name = form.first_name.data
        dob = form.dob.data
        email = form.email.data
        User.create(username=username, password=password,
                    first_name=first_name, dob=dob,
                    email=email)
        flash('Registration is successful! Please login.')
        return redirect(url_for('login'))

    else:
        flash('This username is not available')
        return redirect(url_for('registration'))


@auth.route('/update_user')
@login_required
def update_user():
    form_error = request.cookies.get('form_error')
    try:
        form_error = json.loads(form_error)
    except TypeError or AttributeError:
        form_error = dict()

    form = UpdateUserForm()
    for attr in form.get_attributes():
        if attr in request.user.get_attributes():
            cur_value = getattr(request.user, attr)
            if cur_value != getattr(User, attr).default:
                getattr(form, attr).data = cur_value

    for attr in form.get_attributes():
        getattr(form, attr).saved_error = form_error.get(attr, [])
    r = make_response(render_template('update_user.html', form=form))
    r.delete_cookie('form_error')
    return r


@auth.route('/update_user/processing', methods=['POST'])
@login_required
def update_user_processing():
    form = UpdateUserForm(request.form)
    if not form.validate():
        flash('Error: incorrect entry in the form')
        r = make_response(redirect(url_for('update_user')))
        r.set_cookie('form_error', json.dumps(form.errors))
        return r

    print(f'Data is {form.data}')
    print(f'Entered username is {form.username.data}')
    print(f'Entered password is {form.cur_password.data}')
    if request.user.verify_password(form.cur_password.data):
        data = dict()
        for attr in form.get_attributes():
            data[attr] = getattr(form, attr).data
        request.user.update(**data)

        encrypted_username = crypting.aes_encrypt(form.username.data)
        r = make_response(redirect(url_for('blogpost_recent')))
        r.set_cookie('username', encrypted_username)
        r.set_cookie('first_name', form.first_name.data)
        flash('You are successfully logged in!')
        return r
    else:
        flash("Incorrect credentials: please double-check password")
        return redirect(url_for('update_user'))

