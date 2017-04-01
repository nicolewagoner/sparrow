import os


class BaseConfig(object):
    SECRET_KEY = os.environ['SECRET_KEY']
    SENTRY_DSN = os.environ['SENTRY_DSN']
