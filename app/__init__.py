from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'secretkey'




db = SQLAlchemy(app)
class Users(db.Model, UserMixin):
    __tablename__ = "Users"
    pesel = db.Column(db.String(11), primary_key=True, unique=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    login = db.Column(db.String(15), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    phone_number = db.Column(db.String(9), nullable=False)
    account_active = db.Column(db.Boolean, nullable=False)
    residence_address = db.Column(db.String(100), nullable=False)

    def get_id(self):
        return self.pesel

class Customers(db.Model, UserMixin):
    __tablename__ = "Customers"
    customer_id = db.Column(db.String(16), primary_key=True, unique=True)
    iban_number = db.Column(db.String(28), nullable=False, unique=True)
    account_balance = db.Column(db.Float, nullable=False)
    pesel = db.Column(db.String(11), db.ForeignKey('Users.pesel'))

class PersonalData(db.Model, UserMixin):
    __tablename__ = "PersonalData"
    date_of_birth = db.Column(db.DateTime, nullable=False)
    date_of_issue_of_id = db.Column(db.DateTime, nullable=False)
    expiry_date_of_id = db.Column(db.DateTime, nullable=False)
    place_of_birth = db.Column(db.String(50), nullable=False)
    father_name = db.Column(db.String(50), nullable=False)
    mother_name = db.Column(db.String(50), nullable=False)
    id_card_number = db.Column(db.String(9), nullable=False,primary_key=True, unique=True)
    issuing_authority = db.Column(db.String(30), nullable=False)
    nationality = db.Column(db.String(30), nullable=False)
    sex = db.Column(db.String(1), nullable=False)
    customer_id = db.Column(db.String(16), db.ForeignKey('Customers.customer_id'))

class Employees(db.Model):
    __tablename__ = "Employees"
    employee_id = db.Column(db.String(16), primary_key=True, unique=True)
    salary = db.Column(db.Float, nullable=False)
    room = db.Column(db.String(20), nullable=False)
    office = db.Column(db.String(20), nullable=False)
    shift = db.Column(db.Integer, nullable=False)# 0: 0-8, 1: 8-16, 2: 16-0
    pesel = db.Column(db.String(11), db.ForeignKey('Users.pesel'))    

class Admins(db.Model):
    __tablename__ = "Admins"
    admin_id = db.Column(db.String(16), primary_key=True, unique=True)
    employee_id = db.Column(db.String(16), db.ForeignKey('Employees.employee_id'))

class CustomerServiceEmployees(db.Model):
    __tablename__ = "CustomerServiceEmployees"
    cse_id = db.Column(db.String(16), primary_key=True, unique=True)
    employee_id = db.Column(db.String(16), db.ForeignKey('Employees.employee_id'))

class Messages(db.Model):
    __tablename__ = "Messages"
    message_id = db.Column(db.String(16), primary_key=True, unique=True)
    content = db.Column(db.String(1000), nullable=False)
    date = db.Column(db.DateTime, nullable=False)

    customer_id = db.Column(db.String(16), db.ForeignKey('Customers.customer_id'), nullable=False)
    cse_id = db.Column(db.String(16), db.ForeignKey('CustomerServiceEmployees.cse_id'), nullable=False)

class Transfers(db.Model):
    __tablename__ = "Transfers"
    transfer_id = db.Column(db.String(64), primary_key=True, unique=True)
    sender_iban = db.Column(db.String(28), nullable=False)
    receiver_iban = db.Column(db.String(28), nullable=False)
    title = db.Column(db.String(50), nullable=False)
    receiver_name = db.Column(db.String(50), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    sender_id = db.Column(db.String(16), db.ForeignKey('Customers.customer_id'), nullable=False)

with app.app_context():
    db.create_all()

bcrypt = Bcrypt(app)