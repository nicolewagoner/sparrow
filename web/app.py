from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from config import BaseConfig

app = Flask(__name__)
app.config.from_object(BaseConfig)

try:
    client = MongoClient('mongodb', 27017)
except ConnectionFailure:
    print("Server not available")


@app.route('/')
def hello_world():
    return 'Hello World!!!'


@app.route('/user', methods=['GET'])
def get_all_users():
    user_db = client.test.user

    output = []
    for user in user_db.find():
        output.append({
            'first_name': user['first_name'],
            'last_name': user['last_name']
        })
    return jsonify({'result': output})


@app.route('/user', methods=['POST'])
def add_user():
    user_db = client.test.user

    first_name = request.form['first_name']
    last_name = request.form['last_name']

    result = user_db.insert_one({
        'first_name': first_name,
        'last_name': last_name
    })
    result_id = result.inserted_id

    inserted_test = user_db.find_one({'_id': result_id})
    output = {
        'first_name': inserted_test['first_name'],
        'last_name': inserted_test['last_name']
    }
    return jsonify({'result': output})


@app.route('/user/<first_name>', methods=['GET'])
def get_one_user(first_name):
    user_db = client.test.user

    user = user_db.find_one({'first_name': first_name})
    if user:
        output = {
            'first_name': user['first_name'],
            'last_name': user['last_name']
        }
        return jsonify({'result': output})
    else:
        return render_template('user.html', first_name=first_name)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
