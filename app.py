import smtplib
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, validators
from wtforms.validators import  Length, EqualTo, Email, ValidationError, InputRequired, ValidationError
from flask_bcrypt import Bcrypt

app = Flask(__name__,
            template_folder='templates',
            static_url_path='/static',
            )

# pass encryption method
bcrypt = Bcrypt(app)

# Using smtplib to send emails to new users

with open("instance/app_pw.txt", "r") as file:
    app_password = file.read()
my_email = "programnet2@gmail.com"
app_password = app_password.strip()

with open("instance/secret_key.txt", "r") as file:
    secret_key = file.read()

# configuration for the app database
app.config['SECRET_KEY'] =secret_key.strip()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# Flask-Login setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# User model
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.String(70), nullable=False)
    first_name = db.Column(db.String(35), nullable=False)

# Registration and Login forms
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

class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=True)
    email = db.Column(db.String(120), nullable=True)
    rating = db.Column(db.Integer, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    comments = db.Column(db.Text, nullable=False)
    subscribe = db.Column(db.Boolean, default=False)
    submitted_at = db.Column(db.DateTime, default=datetime.now)
    
    def __repr__(self):
        return f'<Feedback {self.id} from {self.name}>'
# Checks to see if the email has already been registered



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
def register():
    form = RegistrationForm()
    password = form.password.data
    confirm_password = form.confirm_password.data
    email = form.email.data

    existing_user = User.query.filter_by(email=form.email.data).first()

    if existing_user:
        flash('Email already registered. Please log in.', 'danger')
        return redirect(url_for('login'))
    if form.validate_on_submit():
            if password != confirm_password:
                flash('Passwords do not match', 'danger')
                return redirect(url_for('register'))
            else:
                hashed_password = bcrypt.generate_password_hash(form.password.data)
                new_user = User(email=form.email.data, password=hashed_password, first_name=form.first_name.data)
                db.session.add(new_user)
                welcome_email(form.email.data, "Welcome to our platform", "Thank you for signing up!")
                db.session.add(new_user)
                db.session.commit()
                flash('Registration successful! Please log in.', 'success')
                return redirect(url_for('login'))

    return render_template('register.html', form=form)

@app.route('/login', methods =['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        # checking is password with stored hash
        if user and bcrypt.check_password_hash(user.password, form.password.data):
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
        # check if the user is already logged in
        if not current_user.is_authenticated:
            flash('Please log in to access the dashboard.', 'danger')
            return redirect(url_for('login'))
        return render_template('dashboard.html', name=current_user.first_name)



@app.route('/roadmap')
def roadmap():
    return render_template('roadmap.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))

@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if request.method == 'POST':
        name = request.form.get('name', 'Anonymous')
        email = request.form.get('email', '')
        rating = request.form.get('rating')
        category = request.form.get('category')
        comments = request.form.get('comments')
        subscribe = 'subscribe' in request.form
        
        # Validation
        if not rating or not category or not comments:
            flash('Please fill in all required fields', 'error')
            return redirect(url_for('feedback'))
        
        try:
            # Create new feedback record
            new_feedback = Feedback(
                name=name,
                email=email,
                rating=rating,
                category=category,
                comments=comments,
                subscribe=subscribe,
                submitted_at=datetime.now()
            )
            db.session.add(new_feedback)
            db.session.commit()
            
            flash('Thank you for your feedback!', 'success')
            return redirect(url_for('feedback_thank_you'))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while submitting your feedback', 'error')
            return redirect(url_for('feedback'))
    
    # If GET request, just show the form
    return render_template('feedback.html')

@app.route('/feedback/thank-you')
def feedback_thank_you():
    return render_template('feedback_thanks.html')




if __name__ == '__main__':
    app.run(debug = True)