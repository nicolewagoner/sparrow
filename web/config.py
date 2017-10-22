import os


class BaseConfig(object):
    SECRET_KEY = os.environ['SECRET_KEY']
    SENTRY_DSN = os.environ['SENTRY_DSN']

    SPOTIFY_CLIENT_ID = os.environ['SPOTIFY_CLIENT_ID']
    SPOTIFY_CLIENT_SECRET = os.environ['SPOTIFY_CLIENT_SECRET']
    SPOTIFY_REDIRECT_URL = os.environ['SPOTIFY_REDIRECT_URL']

    GOOGLE_GEOCODING = os.environ['GOOGLE_GEOCODING']
