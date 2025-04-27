import smtplib
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, validators
from wtforms.validators import  Length, EqualTo, Email, ValidationError, InputRequired, ValidationError
from werkzeug.security import generate_password_hash, check_password_hash
from flask_bcrypt import Bcrypt
import os
if os.path.exists('database.db'):
    os.remove('database.db')
app = Flask(__name__,
            template_folder='templates',
            static_url_path='/static',
            )
bcrypt = Bcrypt(app)

my_email = "programnet2@gmail.com"
app_password = "zfch tqsd edxr hfqw"

app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.String(70), nullable=False)
    first_name = db.Column(db.String(35), nullable=False)

class RegistrationForm(FlaskForm):
    first_name = StringField('Name', validators=[InputRequired(), Length(min=2, max=35)], render_kw={'placeholder': 'Name'})
    email = StringField('Email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)], render_kw={'placeholder': 'Email'})
    password = PasswordField('Password', validators=[InputRequired(), Length(min=6, max=35)], render_kw={'placeholder': 'Password'})
    confirm_password = PasswordField('Confirm Password', validators=[InputRequired(), EqualTo('password', message='Passwords must match')], render_kw={'placeholder': 'Confirm Password'})
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)], render_kw={'placeholder': 'Email'})
    password = PasswordField('Password', validators=[InputRequired(), Length(min=6, max=35)], render_kw={'placeholder': 'Password'})
    submit = SubmitField('Login')

def validate_email(self, email):
    user = User.query.filter_by(email=email.data).first()
    if user:
        raise ValidationError('Email already registered. Please use a different email.')    

def welcome_email(to, subject, body):
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(my_email, app_password)
            message = f'Subject: {subject}\n\n{body}'
            server.sendmail(my_email, to, message)
    except Exception as e:
        print(f"Error sending email: {e}")

with app.app_context():
        db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/register', methods=['GET', 'POST'])
def signup():
    form = RegistrationForm()

    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        new_user = User(email=form.email.data, password=hashed_password, first_name=form.first_name.data)
        db.session.add(new_user)
        welcome_email(form.email.data, "Welcome to our platform", "Thank you for signing up!")
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods =['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password', 'danger')


    redirect(url_for('dashboard'))
    return render_template('login.html', form=form)


@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
        return render_template('dashboard.html', name=current_user.first_name)
   







if __name__ == '__main__': 
    app.run(debug = True)