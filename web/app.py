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
def index():
    return render_template('index.html')


# @app.route('/user/', methods=['GET'])
# @app.route('/user/<first_name>', methods=['GET'])
# def get_one_user(first_name=None):
#     user_db = client.test.user
#
#     if first_name is not None:
#         user = user_db.find_one({'first_name': first_name})
#         if user:
#             output = {
#                 'first_name': user['first_name'],
#                 'last_name': user['last_name']
#             }
#             return jsonify({'result': output})
#
#     return render_template('user.html', first_name=first_name)


@app.errorhandler(BadRequest)
def handle_bad_request(e):
    return 'bad request!'


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5002)
