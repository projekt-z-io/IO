from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from app.__init__ import Users, Customers, Employees, CustomerServiceEmployees, Admins
from sqlalchemy.sql import func

def login_is_in_database(login: str) -> bool:
    if Users.query.filter_by(login=login).first() == None:
        return False
    return True

def iban_is_in_database(iban: str) -> bool:
    if Customers.query.filter_by(iban_number=iban).first() == None:
        return False
    return True

def customer_id_is_in_database(customer_id: str) -> bool:
    if Customers.query.filter_by(customer_id=customer_id).first() == None:
        return False
    return True

def email_is_in_database(email: str) -> bool:
    if Users.query.filter_by(email=email).first() == None:
        return False
    return True

def employee_id_is_in_database(employee_id: str) -> bool:
    if Employees.query.filter_by(employee_id=employee_id).first() == None:
        return False
    return True

def cse_id_is_in_database(cse_id: str) -> bool:
    if CustomerServiceEmployees.query.filter_by(cse_id=cse_id).first() == None:
        return False
    return True

def user_is_employee(login: str) -> bool:
    pesel = Users.query.filter_by(login=login).first().pesel
    if  Employees.query.filter_by(pesel=pesel).first() == None:
        return False
    return True