# Authentification blueprint package for flask
[![Build Status](https://travis-ci.org/kate-melnykova/authentication.svg?branch=develop)](https://travis-ci.org/kate-melnykova/authentication)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Blueprint defines object User who can register, log in, and log out.
User can also update its profile. The data is stored on redis database.
## Installing

To install a package, open the terminal and download the GitHub repository:
```
$  pip3 install --user git+https://github.com/kate-melnykova/authentication
```
The database for the package is redis, so please make sure that it is started prior to using the package.

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
from authentication import init_auth_blueprint
import redis

app = Flask(__name__, instance_relative_config=True)
app.secret_key = 'very-secret-key'  # change it

# start redis database
redis_url = 'redis://localhost:6379/0'
r = redis.Redis.from_url(redis_url)

# register blueprint
with app.app_context():
    init_auth_blueprint(redis_url=redis_url)

if __name__ == '__main__':
    app.run(debug=True, host='localhost', port='5000')
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
$ python3 app.py
```
The server will run the app. Note that only pages 'login', '
logout', 'register', and 'update_user' exist.
