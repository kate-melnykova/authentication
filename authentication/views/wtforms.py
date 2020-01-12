from typing import List

from wtforms import Form
from wtforms import StringField
from wtforms import Field, PasswordField, BooleanField, DateField, TextAreaField
from wtforms.fields.html5 import EmailField
from wtforms import validators


strip_filter = lambda x: x.strip() if x else None


class FormwAttributes(Form):
    def get_attributes(self) -> List[str]:
        attrs = []
        for k, v in self.__dict__.items():
            if isinstance(v, Field):
                attrs.append(k)
        return attrs

class LoginForm(FormwAttributes):
    username = StringField('Username', [validators.Length(min=4, max=15)])
    password = PasswordField('Password', [validators.Length(min=6, max=15)])
    rememberme = BooleanField('Remember me?')


class RegistrationForm(FormwAttributes):
    username = StringField('Username', [validators.InputRequired(), validators.Length(min=4, max=15)])
    password = PasswordField('Password', [validators.InputRequired(), validators.Length(min=6, max=15)])
    confirm = PasswordField('Repeat Password',
                            [validators.InputRequired(),
                             validators.EqualTo('password', message='Passwords must match')])
    first_name = StringField('First name', [validators.Optional(), validators.Length(min=1, max=15)])
    dob = DateField('Date of birth in format Y-M-D', [validators.Optional()], format='%Y-%m-%d')
    email = EmailField('Email', [validators.Optional(), validators.Length(min=6, max=50), validators.Email()])

    # TODO check Form.data
    def get_attributes(self) -> List[str]:
        attrs = []
        for k, v in self.__dict__.items():
            if isinstance(v, Field):
                attrs.append(k)
        return attrs


class UpdateUserForm(FormwAttributes):
    username = StringField('Username', render_kw={'disabled': ''})
    cur_password = PasswordField('Current password', [validators.InputRequired(), validators.Length(min=6, max=15)])
    password = PasswordField('New password (optional)', [validators.Optional(), validators.Length(min=6, max=15)])
    confirm = PasswordField('Repeat Password',
                            [validators.Optional(),
                             validators.EqualTo('password', message='Passwords must match')])
    first_name = StringField('First name', [validators.Optional(), validators.Length(min=1, max=15)])
    dob = DateField('Date of birth in format Y-M-D', [validators.Optional()], format='%Y-%m-%d')
    email = EmailField('Email', [validators.Optional(), validators.Length(min=6, max=50), validators.Email()])

    def get_attributes(self) -> List[str]:
        attrs = []
        for k, v in self.__dict__.items():
            if isinstance(v, Field):
                attrs.append(k)
        return attrs


class BlogForm(FormwAttributes):
    title = StringField('Title', [validators.Length(min=1, max=255)],
                        filters=[strip_filter])
    content = TextAreaField('Content', filters=[strip_filter])
    id = None