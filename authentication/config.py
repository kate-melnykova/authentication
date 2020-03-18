"""
    authentication.config
    ~~~~~~~~~~~~
    Implements the configuration related objects.
"""
settings = {
    'FLOGGY_REDIS_URL': '',
    'UPLOAD_FOLDER': '/media',
    'ALLOWED_PHOTO_EXTENSIONS': ['jpg'],
    'REDIRECT_AFTER_LOGIN': 'welcome',
    'LOGIN_URL': 'login',
    'REG_URL': 'registration',
    'LOGOUT_URL': 'logout',
    'UPDATE_URL': 'update_user',
}
