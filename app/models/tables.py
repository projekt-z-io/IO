from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from app.__init__ import Users, Customers
from sqlalchemy.sql import func

def login_is_in_database(login: str) -> bool:
    if Users.query.filter_by(login=login).first() == None:
        return False
    return True

def iban_is_in_database(iban: str) -> bool:
    if Customers.query.filter_by(iban_number=iban).first() == None:
        return False
    return True

def find_max_customer_id() -> str:
    return Customers.query.with_entities(func.max(Customers.customer_id)).scalar()

def email_is_in_database(email: str) -> bool:
    if Users.query.filter_by(email=email).first() == None:
        return False
    return True

