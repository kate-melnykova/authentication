from flask import current_app


def init_auth_blueprint(config_file='config.py', redis_url='') -> None:
    if not redis_url:
        redis_url = current_app.config.get('REDIS_URL', 'redis://redis:6379/0')

    from authentication.models.db import db
    db.connect(url=redis_url)

    from authentication import app
    current_app.register_blueprint(app.auth)
    app.auth.config.from_object(config_file)



