from flask import Flask
from flask import render_template, make_response, request, json
import json
import connexion
import database
import datetime
from flask_cors import CORS

app = Flask(__name__)
CORS(app, supports_credentials=True)
config = None

@app.route('/api/register', methods=['POST'])
def register():
    resp = make_response()

    if request == None:
        return resp, 400
    
    if request.json == None:
        return resp, 400

    if 'username' not in request.json \
        or 'password' not in request.json \
        or 'email' not in request.json \
        or 'first_name' not in request.json \
        or 'last_name' not in request.json:
        return resp, 400

    try:
        database.DB().register(request.json['username'],
            request.json['password'],
            request.json['email'],
            request.json['first_name'],
            request.json['last_name'])

        return resp, 200
    except Exception as e:
        resp = app.response_class(
            response=json.dumps(
                {
                    'error' : str(e)
                }
            ),
            mimetype='application/json'
        )

        return resp, 400

@app.route('/')
def home():
    return render_template('home.html')

if __name__ == '__main__':
    try:
        with open('config.json', 'rt') as inputfile:
            config = json.load(inputfile)
    except Exception:
        print('ERROR: Configuration file is missing!')
        exit(-1)

    app.run(host=config['backend']['host'],
            port=config['backend']['port'], debug=True)
