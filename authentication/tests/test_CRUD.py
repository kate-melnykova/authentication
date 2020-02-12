from time import time, mktime
from datetime import datetime
from unittest.mock import patch, Mock, MagicMock

import pytest
from passlib.hash import sha256_crypt

# from app.app import app
from authentication.auth.models import User, AnonymousUser

import json
from authentication.models.db import db

#app.testing = True
#@pytest.fixture
#def client():
#    test_client = app.test_client()
#    yield test_client

time = datetime.now()


user_data_sample = {
    'username': 'myusername',
    'password': 'mypassword',
    'first_name': 'name',
    'dob': datetime(year=2000, month=1, day=10),
    'email': 'myemail@mydomain.com'
}


#@patch('app.auth.models.User.get_connection')
@patch('authentication.models.db.DB.save')
def test_create_method_returns_a_valid_user_object(_):
    user = User.create(**user_data_sample)
    assert isinstance(user, User), 'user is not an instance of User'
    assert isinstance(user.dob, datetime), 'user.dob is not in datetime format'
    assert isinstance(user.username, str), 'user.username is not a string'
    assert isinstance(user.id, str), 'user.id is not a string'

    assert user.id == f'user:{user_data_sample["username"]}', 'user.id does not align well with username'
    assert sha256_crypt.verify(user_data_sample['password'], user.password),\
        'original password is not verified by hashed password'


db_sample_user = b'{"id": "user:username",' \
                 b' "password": "hashed_secret_password",' \
                 b' "first_name": "first name",' \
                 b' "dob": 600000000.0,' \
                 b' "email": "fake_email@email.com",' \
                 b' "date": 1570000000,' \
                 b' "username": "myusername"}'


#@patch('authentication.models.db.DB.load',
#       return_value=MagicMock(**{'get.return_value': db_sample_user}))
@patch('authentication.models.db.DB.load', return_value=db_sample_user)
def test_load_user_form_db_returns_object_in_python_format(_):
    json.loads(db_sample_user)

    user = User.load(username='')
    assert isinstance(user.id, str), 'user.id is not a string'
    assert isinstance(user.password, str), 'user.password is not a string'
    assert isinstance(user.first_name, str), 'user.first_name is not a string'
    assert isinstance(user.dob, datetime), 'user.dob is not a datetime'
    assert isinstance(user.email, str), 'user.email is not a string'
    assert isinstance(user.date, datetime), 'user.date is not a datetime'
    assert isinstance(user.username, str), 'user.username is not a string'

"""
current_time = time()
user = User(username='username',
            password='hashed_password',
            id='user:username',
            dob=current_time,
            date=current_time)

@patch('app.auth.models.User.get_connection')
@patch('model.db.redis.set')
def test_save_user_from_user_object_to_db(_, writer):
    user.save()
    writer.assert_call_once_with(b'"id": "user:username",'
                                 b'"username": "username",'
                                 b'"password": "hashed_password",'
                                 b'"first_name": "",'
                                 b'"dob": "' + str(int(mktime(current_time.timetuple()))) + b'",' +
                                 b'"email": "",'
                                 b'"date": ' + str(int(mktime(current_time.timetuple()))) + b'"')
"""
