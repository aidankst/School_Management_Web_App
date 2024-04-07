import os
import random
from flask_migrate import Migrate
from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Boolean, Table, BIGINT, create_engine
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, LoginManager, login_required, logout_user, current_user
from functools import wraps

load_dotenv()

from flask_sqlalchemy import SQLAlchemy

db_url = os.getenv('DATABASE_URL')
app = Flask(__name__)

app.config['SECRET_KEY'] = 'school_management_app'
app.config['SQLALCHEMY_DATABASE_URI'] = db_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
UPLOAD_FOLDER = '/static/images/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


db = SQLAlchemy(app)
migrate = Migrate(app, db)

# conn = psycopg2.connect(db)

@app.context_processor
def inject_datetime():
    return {'datetime': datetime}


student_course_association = Table('student_course_association', db.Model.metadata,
    Column('student_id', Integer, ForeignKey('student.id')),
    Column('course_id', Integer, ForeignKey('course.id'))
)


class User(UserMixin, db.Model):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, unique=True)
    name = Column(String(80), nullable=False)
    email = Column(String(120), nullable=False, unique=True)
    password = Column(String(120), nullable=False)
    role = Column(String(20), nullable=False)
    phone = Column(String(15), nullable=False)
    is_verified = Column(Boolean, default=False)
    status = Column(String(20), nullable=True)
    start_date = Column(DateTime, nullable=True)
    end_date = Column(DateTime, nullable=True)

    @staticmethod
    def check_exists(email):
        user = db.session.query(User).filter_by(email=email).first()
        return user is not None
        
    @staticmethod
    def generate_user_id():
        status = True
        while status:
            user_id = random.randint(100000, 999999)
            check = db.session.query(User).filter_by(id=user_id).first()
            if not check:
                status = False
        return user_id

    @staticmethod
    def create_password(password):
        hashed_password = generate_password_hash(
            password,
            method='pbkdf2:sha256',
            salt_length=8,
        )
        return hashed_password

    @staticmethod
    def check_password(email, password):
        user = db.session.query(User).filter_by(email=email).first()
        if user:
            return check_password_hash(user.password, password)
        return False


class Employee(db.Model):
    __tablename__ = 'employee'

    id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    salary = Column(Float, nullable=False)
    salary_info = db.relationship('Salary', backref='employee', lazy=True)


class Student(db.Model):
    __tablename__ = 'student'

    id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    father_name = Column(String(80), nullable=False)
    mother_name = Column(String(80), nullable=False)
    courses = db.relationship('Course', secondary=student_course_association, backref='students', lazy='dynamic')
    payments = db.relationship('Payment', backref='student', lazy=True)
    grades = db.relationship('Grade', backref='student', lazy=True)
    invoices = db.relationship('Invoice', backref='student', lazy=True)



class Course(db.Model):
    id = Column(Integer, primary_key=True, unique=True)
    name = Column(String(80), nullable=False, unique=True)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=True)
    fees = Column(Integer, nullable=False)
    description = Column(String(50), nullable=True)
    status = Column(String(20), nullable=True)
    subjects = db.relationship('Subject', backref='course', lazy=True)
    invoices = db.relationship('Invoice', backref='course', lazy=True)


class Subject(db.Model):
    id = Column(Integer, primary_key=True, unique=True)
    name = Column(String(80), nullable=False)
    description = Column(String(50), nullable=True)
    course_id = Column(Integer, ForeignKey('course.id'), nullable=False)
    grades = db.relationship('Grade', backref='subject', lazy=True)


class Payment(db.Model):
    id = Column(BIGINT, primary_key=True, unique=True)
    student_id = Column(Integer, ForeignKey('student.id'), nullable=False)
    amount = Column(Float, nullable=False)
    date = Column(DateTime, nullable=False)
    attending_days = Column(Integer, nullable=False)
    payment_registerer = Column(String(80), nullable=False)


class Invoice(db.Model):
    id = Column(BIGINT, primary_key=True, unique=True)
    student_id = Column(Integer, ForeignKey('student.id'), nullable=False)
    course_id = Column(Integer, ForeignKey('course.id'), nullable=False)
    amount = Column(Float, nullable=False)
    date = Column(DateTime, nullable=False)
    issuer = Column(String(80), nullable=False)
    deadline = Column(DateTime, nullable=False)
    status = Column(String(20), nullable=True)
    attending_days = Column(Integer, nullable=False)


class Grade(db.Model):
    id = Column(Integer, primary_key=True, unique=True)
    student_id = Column(Integer, ForeignKey('student.id'), nullable=False)
    subject_id = Column(Integer, ForeignKey('subject.id'), nullable=False)
    month = Column(String(15), nullable=False)
    score = Column(Float, nullable=False)


class Salary(db.Model):
    id = Column(Integer, primary_key=True, unique=True)
    employee_id = Column(Integer, ForeignKey('employee.id'), nullable=False)
    amount = Column(Float, nullable=False)
    date = Column(DateTime, nullable=False)



with app.app_context():
        db.create_all()


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    user = db.session.query(User).get(user_id)
    return user

def requires_roles(*roles):
    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            # Check if role is not set or if the role is not allowed
            if not current_user.is_authenticated or current_user.role not in roles:
                return render_template('/master/index/unauthorized.html', logged_in=True)
            return fn(*args, **kwargs)
        return decorated_view
    return wrapper


@app.route('/')
def index():
    return render_template('/master/auth/login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# if __name__ == '__main__':
#     # Create database tables if they don't exist
#     app.run(debug=True)