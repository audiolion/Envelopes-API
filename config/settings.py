import os
from apistar_jwt.authentication import JWTAuthentication
from utils.renderers import JSONRenderer

settings = {
    'AUTHENTICATION': [JWTAuthentication()],
    'DATABASES': {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.environ.get('DB_NAME'),
            'HOST': os.environ.get('DB_HOST'),
            'USER': os.environ.get('DB_USER'),
            'PASSWORD': os.environ.get('DB_PASS'),
        },
    },
    'INSTALLED_APPS': [
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'envelopes.apps.EnvelopesConfig',
        'behaviors.apps.BehaviorsConfig',
        'improved_user.apps.ImprovedUserConfig',
    ],
    'AUTH_USER_MODEL': 'improved_user.User',
    'AUTH_PREFIX': '',
    'AUTH_PASSWORD_VALIDATORS': [
        {
            'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
            'OPTIONS': {
                'user_attributes': ('email', 'full_name', 'short_name')
            },
        },
        # include other password validators here
    ],
    'HASHIDS_SALT': os.environ.get('HASHIDS_SALT'),
    'SECRET_KEY': os.environ.get('SECRET_KEY'),
    'JWT': {
        'SECRET': os.environ.get('JWT_SECRET'),
        'ID': 'user',
    },
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME'),
        'HOST': os.environ.get('DB_HOST'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASS'),
    },
}

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'envelopes.apps.EnvelopesConfig',
    'behaviors.apps.BehaviorsConfig',
    'improved_user.apps.ImprovedUserConfig',
]

AUTH_USER_MODEL = 'improved_user.User'

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
        'OPTIONS': {
            'user_attributes': ('email', 'full_name', 'short_name')
        },
    },
]

HASHIDS_SALT = os.environ.get('HASHIDS_SALT')
SECRET_KEY = os.environ.get('SECRET_KEY')
JWT_SECRET = os.environ.get('JWT_SECRET')
