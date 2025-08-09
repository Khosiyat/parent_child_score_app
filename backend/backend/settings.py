import os
from datetime import timedelta

# Add installed apps
INSTALLED_APPS = [
    # default apps ...
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
    'api',  # your app
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    # default middlewares ...
]

# CORS settings for frontend URL (example http://localhost:3000)
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
]

# REST Framework configuration
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
}

# Simple JWT settings (optional customization)
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'AUTH_HEADER_TYPES': ('Bearer',),
}

# Auth user model
AUTH_USER_MODEL = 'api.User'

# Database settings, other settings ...


CELERY_BROKER_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
