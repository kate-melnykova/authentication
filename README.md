# Authentification blueprint package for flask

Blueprint defines object User who can register, log in, and log out.
User can also update its profile. The data is stored on redis database.
## Installing

To install a package, open the terminal and download the GitHub repository:
```
$ git clone https://github.com/kate-melnykova/authentication
```
To install the package, run
```
$ pip install ./authentication/dist/authentication-1.0.tar.gz 
```
Please make sure that `Flask`, `pycryptodome`, `passlib`, `wtforms` is satisfied.

## Getting started
Create a python project with the following minimal structure
```apex
- templates
  -- base.html
- app.py
```

The file `app.py` creates a basic `flask` app and registers the blueprint
```apex
from flask import Flask
from authentication import auth

app = Flask(__name__, instance_relative_config=True)
app.register_blueprint(auth)
```
and `base.html` contains the base style:
```apex
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
    <div>
        {% block form %}
        {% endblock %}
    </div>
</body>
</html>

```
Open the terminal and run 
```apex
$ export FLASK_APP=app.py
$ flask run
```

## Running the tests

Explain how to run the automated tests for this system



## Getting started
