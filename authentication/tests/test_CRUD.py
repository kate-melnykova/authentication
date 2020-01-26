from time import time, mktime
from datetime import datetime
from unittest.mock import patch, Mock, MagicMock

import pytest
from passlib.hash import sha256_crypt

# from app.app import app
from authentication.auth.models import User, AnonymousUser

#app.testing = True
#@pytest.fixture
#def client():
#    test_client = app.test_client()
#    yield test_client

time = datetime.now()


user_data_sample = {
    'username': 'username',
    'password': 'password',
    'dob': datetime.now()
}


@patch('app.auth.models.User.get_connection')
@patch('app.auth.models.User.save')
def test_create_method_returns_a_valid_user_object(_, __):
    user = User.create(**user_data_sample)
    assert isinstance(user, User), 'user is not an instance of User'
    assert isinstance(user.dob, datetime), 'user.dob is not in datetime format'
    assert isinstance(user.username, str), 'user.username is not a string'
    assert isinstance(user.id, str), 'user.id is not a string'

    assert user.id == f'user:{user_data_sample["username"]}', 'user.id does not align well with username'
    assert sha256_crypt.verify(user_data_sample['password'], user.password),\
        'original password is not verified by hashed password'


post_data_sample = {
    'title': 'title',
    'author': 'author',
    'content': 'content',
    'author_id': 'user:author'
}


@patch('app.content.models.BlogPost.get_connection')
@patch('app.content.models.BlogPost.save')
def test_create_method_returns_a_valid_blogpost_object(_, __):
    post = BlogPost.create(**post_data_sample)
    assert post.author is not None
    assert isinstance(post.author, str), 'Author of post is not a string'
    assert isinstance(post.title, str), 'Title of post is not a string'
    assert isinstance(post.content, str), 'Content of post is not a string'
    assert isinstance(post.id, str), 'post.id is not a string'
    assert isinstance(post.author_id, str), 'post.author_id is not a string'

    assert post.author_id == f'user:{post_data_sample["author"]}',\
        'post.author_id and post.author are not well-aligned'
    assert post.id.startswith('blogpost:'), 'Post.id does not start with "blogpost:"'
    assert post.id.endswith(f':{post_data_sample["author"]}'), 'post.id does not end with username'
    assert len(post.id) == len('blogpost:') + 8 + 1 + len(post_data_sample['author']), 'Length of post.id is incorrect'


db_sample_user = b'{"id": "user:username",' \
                 b' "password": "hashed_secret_password",' \
                 b' "first_name": "first name",' \
                 b' "dob": 600000000.0,' \
                 b' "email": "fake_email@email.com",' \
                 b' "date": 1570000000,' \
                 b' "username": "username"}'


@patch('app.auth.models.User.get_connection',
       return_value=MagicMock(**{'get.return_value': db_sample_user}))
def test_load_user_form_db_returns_object_in_python_format(_):
    user = User.load(username='')
    assert isinstance(user.id, str), 'user.id is not a string'
    assert isinstance(user.password, str), 'user.password is not a string'
    assert isinstance(user.first_name, str), 'user.first_name is not a string'
    assert isinstance(user.dob, datetime), 'user.dob is not a datetime'
    assert isinstance(user.email, str), 'user.email is not a string'
    assert isinstance(user.date, datetime), 'user.date is not a datetime'
    assert isinstance(user.username, str), 'user.username is not a string'


db_sample_blogpost =  b'{"id": "blogpost:sample_id",' \
                      b' "author_id": "user:username",' \
                      b' "title": "Post title",' \
                      b' "content": "Post content",' \
                      b' "author": "username"}'


@patch('app.content.models.BlogPost.get_connection')
@patch('app.models.db.redis.get', return_value=db_sample_blogpost)
def test_load_blogpost_form_db_returns_object_in_python_format(_, __):
    post = BlogPost.load(db_sample_blogpost)
    assert isinstance(post.id, str), 'post.id is not a string'
    assert isinstance(post.author_id, str), 'post.author_id is not a string'
    assert isinstance(post.title, str), 'post.title is not a string'
    # assert isinstance(post.content, ManualType)
    assert isinstance(post.author, str), 'post.author is not a string'

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
