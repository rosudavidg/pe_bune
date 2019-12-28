from flask import Flask
from flask import render_template, make_response, request, json, send_from_directory, redirect, url_for, session, flash
import json
import database
import datetime
import time
import os
from flask_cors import CORS
from models.user import User

app = Flask(__name__)
app.secret_key = "dabumts secret key"
CORS(app, supports_credentials=True)
config = None

@app.route('/home', methods=['POST', 'GET'])
def home():
    try:
        # Check if user is logged in
        username = database.DB().is_user_logged_in(request)

        if username == None:
            return redirect('/login')

        # If user is admin
        if database.DB().is_user_admin(username):
            # Compute quizzes
            data = database.DB().get_quizzes()
            resp = make_response(render_template('home_admin.html', result=data))

            return resp, 200
        
        # TODO:
        # If user is not admin
        user = database.DB().get_user(username)
        return make_response(render_template('home_user.html', result=user)), 200
        
    except Exception as e:
        return render_template('login.html'), 400

    return render_template('home.html', result=request.form)

@app.route('/game', methods=['POST', 'GET'])
def game():
    try:
        username = database.DB().is_user_logged_in(request)

        if username == None:
            return redirect('/login')

        game_id = None

        if database.DB().game_exists(username):
            game_id = database.DB().get_game_id(username)
        else:
            game_id = database.DB().create_game(username)
        
        game_quizzes = database.DB().get_game_quizzes(game_id)

        for quiz in game_quizzes:
            quiz['category'] = database.DB().get_category(quiz['quiz_id'])

        return make_response(render_template('game.html', result=game_quizzes)), 200

    except Exception as e:
        return render_template('login.html'), 400

    return username, 200

@app.route('/quiz/<quiz_id>', methods=['POST', 'GET'])
def quiz(quiz_id):
    try:
        username = database.DB().is_user_logged_in(request)

        if username == None:
            return redirect('/login')

        # if database.DB().game_exists(username):
        #     game_id = database.DB().get_game_id(username)
        # else:
        #     game_id = database.DB().create_game(username)
        
        # game_quizzes = database.DB().get_game_quizzes(game_id)

        # for quiz in game_quizzes:
        #     quiz['category'] = database.DB().get_category(quiz['quiz_id'])
        # return str(), 200
        e = database.DB().get_quiz(quiz_id)

        return make_response(render_template('quiz.html', result=e)), 200

    except Exception as e:
        return render_template('login.html'), 400

    return username, 200

@app.route('/logout', methods=['POST', 'GET'])
def web_logout():
    resp = make_response(redirect('/login'))

    resp.set_cookie(key='pebune_token',
        value='',
        expires=0,
        httponly=False)

    return resp

@app.route('/delete', methods=['POST', 'GET'])
def web_delete():
    try:
        question_id = request.form['question_id']

        database.DB().delete_quiz(question_id)

        data = database.DB().get_quizzes()

        return redirect(url_for('home'))

    except Exception as e:
        return render_template('login.html'), 400

@app.route('/add', methods=['POST', 'GET'])
def web_add():
    try:
        category = request.form['category']
        question = request.form['question']
        correct_answer = request.form['correct_answer']
        wrong_answer_1 = request.form['wrong_answer_1']
        wrong_answer_2 = request.form['wrong_answer_2']

        database.DB().add_quiz(category, question, correct_answer, wrong_answer_1, wrong_answer_2)

        data = database.DB().get_quizzes()
        return redirect(url_for('home'))
    except Exception as e:
        return render_template('login.html'), 200

    # return render_template('home.html', result=request.form)

@app.route('/login', methods=['POST', 'GET'])
def web_login():
    try:
        # Check if user is logged in
        if database.DB().is_user_logged_in(request) != None:
            return redirect('/home')

        # Check for credentials
        if request.form != None and 'username' in request.form and 'password' in request.form:
            # Check if user just logged in
            username = request.form['username']
            password = request.form['password']

            res = database.DB().login(username, password)
            
            # Log in - failed
            if res == None:
                return render_template('login.html', result=request.form), 403
            
            # Log in - success
            token, expiration_date = res
            resp = make_response(redirect('/home'))

            resp.set_cookie(key='pebune_token',
                value=token,
                expires=datetime.datetime.strptime(expiration_date, '%Y-%m-%d %H:%M:%S'),
                httponly=False)
            
            return resp
    except Exception as e:
        return render_template('login.html'), 400

    return render_template('login.html')

@app.route('/register', methods=['POST', 'GET'])
def web_register(errors=[]):

    if request.method == "POST":
        errors = False

        username = request.form['username']
        password1 = request.form['password1']
        password2 = request.form['password2']
        email = request.form['email']
        firstname = request.form['firstname']
        lastname = request.form['lastname']

        if len(username) < 8:
            errors = True
            flash("Username must be at least 8 characters", "warning")

        if len(password1) < 8:
            errors = True
            flash("Password must be at least 8 characters", "warning")

        if password1 != password2:
            errors = True
            flash("Passwords differ", "warning")

        if errors:
            return render_template('register.html', result=request.form), 200

        try:
            database.DB().register(username,
                password1,
                email,
                firstname,
                lastname)
            
            database.DB().send_activation_link(email)

            return redirect('register/success')
        except Exception as e:
            flash("Registration failed.", "warning")
            return redirect(request.url)

    return render_template('register.html'), 200

@app.route('/register/success', methods=['POST', 'GET'])
def web_register_success():
    return render_template('registration_success.html'), 200

@app.route('/')
def web_root():
    return redirect('/login')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'templates'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

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
