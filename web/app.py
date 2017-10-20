from flask import Flask, render_template, request, jsonify, flash, url_for, \
    redirect
from config import BaseConfig
from raven.contrib.flask import Sentry
from werkzeug.exceptions import BadRequest

app = Flask(__name__)
app.config.from_object(BaseConfig)
sentry = Sentry(
    app,
    dsn=BaseConfig.SENTRY_DSN
)


@app.route('/')
def hello_world():
    return 'Hello World!!!'


@app.errorhandler(BadRequest)
def handle_bad_request(e):
    return 'bad request!'


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5002)
