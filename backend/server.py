from flask import Flask
from flask import render_template, make_response, request, json
import json
import connexion
import database
import datetime
import time
from flask_cors import CORS

app = Flask(__name__)
app.secret_key = "dabumts secret key"
CORS(app, supports_credentials=True)
config = None

@app.route('/')
def home():
    return render_template('home.html')

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
        
        database.DB().send_activation_link(request.json['email'])

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

@app.route('/api/confirm/<token>', methods=['GET'])
def confirm(token):
    resp = make_response()
    
    try:
        result = database.DB().confirm_user(token)
        
        if result:
            return render_template('confirm.html', message='Email confirmed!'), 200
        else:
            return render_template('confirm.html', message='This link is not valid.'), 410

    except Exception as e:
        resp = app.response_class(
            response=json.dumps(
                {
                    'error' : str(e)
                }
            ),
            mimetype='application/json'
        )

        return resp, 404

@app.route('/api/login', methods=['POST'])
def login():
    resp = make_response()

    if request == None:
        return resp, 400
    
    if request.json == None:
        return resp, 400

    if 'username' not in request.json \
        or 'password' not in request.json:
        return resp, 400

    try:
        res = database.DB().login(request.json['username'],
            request.json['password'])
        
        if res == None:
            return resp, 403
        
        token, expiration_date = res

        resp.set_cookie(key='pebune_token',
            value=token,
            expires=datetime.datetime.strptime(expiration_date, '%Y-%m-%d %H:%M:%S'),
            httponly=False)

        print(datetime.datetime.now())
        print(expiration_date)

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

if __name__ == '__main__':
    try:
        with open('config.json', 'rt') as inputfile:
            config = json.load(inputfile)
    except Exception:
        print('ERROR: Configuration file is missing!')
        exit(-1)

    app.run(host=config['backend']['host'],
            port=config['backend']['port'], debug=True)#, ssl_context='adhoc')
