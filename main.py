from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
import os
import jinja2

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape=True) 

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLAlCHEMY_DATABASE_URI'] = 'mysql+pymysql://user-signup:beproductive@localhost:8889/user-signup'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

@app.route("/")
def index():
    return render_template('signup.html', title="User Signup")

@app.route("/", methods=['POST'])
def validate_submit():
    user_name = request.form['user']
    password = request.form['password']
    password_verify = request.form['password_verify']
    email = request.form['email']

    user_error = ''
    password_error = ''
    password_verify_error = ''
    email_error = ''

    if not " " in user_name:
        if len(user_name) < 3 or len(user_name) > 20:
            user_error = "User name must be between 3 and 20 characters with no spaces. Please try again!"
    else:
        user_error = "User name must be between 3 and 20 characters with no spaces. Please try again!"

    if not " " in password:
        if len(password) < 3 or len(user_name) > 20:
            password_error = "Password must be between 3 and 20 characters with no spaces. Please try again!"
    else:
        password_error = "Password must be between 3 and 20 characters with no spaces. Please try again!" 
    
    if password != password_verify:
        password_verify_error = "Passwords do not match."

    if len(email) == 0:
        email_error = ''
    elif not " " in email:
        if len(email) >= 3 and len(email) <= 20:
            if "@" in email and "." in email:
                email_error = ''
            else:
                email_error = "Email can be blank or must contain '@' and '.' to be valid. Please try again!"
        else:
            email_error = "Email can be blank or must contain '@' and '.' to be valid. Please try again!"
    else:
        email_error = "Email can be blank or must contain '@' and '.' to be valid. Please try again!"

    if not user_error and not password_error and not password_verify_error and not email_error:
        return redirect('/welcome?user={0}'.format(user_name))
    else:
        return render_template("signup.html", user=user_name, email=email, 
    user_error=user_error, password_error=password_error, 
    password_verify_error=password_verify_error, email_error=email_error)

@app.route("/welcome", methods=['GET'])
def welcome_message():
    user_name = request.args.get('user')
    return render_template('welcome.html', user=user_name)


if __name__ == '__main__':
    app.run()