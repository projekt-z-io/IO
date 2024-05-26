import app.models.validators as v
import random
from app.models.tables import iban_is_in_database, login_is_in_database, customer_id_is_in_database, employee_id_is_in_database, cse_id_is_in_database
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from app.__init__ import bcrypt 
import string
from app.__init__ import db, Customers, Transfers, Users, Messages
import datetime


def create_new_iban() -> str:
    for i in range(100):
        iban = 'PL'+''.join(random.choice(string.digits) for _ in range(26))
        if not(iban_is_in_database(iban)):
            return iban
        if i == 99:
            raise Exception('Cannot create new iban. ??????')

def create_new_login() -> str:
    characters = string.ascii_uppercase + string.digits

    for i in range(100):
        login = ''.join(random.choice(characters) for _ in range(15))
        if not(login_is_in_database(login)):
            return login
    raise Exception('Cannot create new login. ??????')

def register_customer(form) -> int:

        if not(v.validate_email(form.email.data)):
            return 1
        if not(form.password.data == form.repeated_password.data):
            return 2
        if not(v.validate_pesel(form.PESEL.data, form.sex.data)):
            return 3
        if not(v.validate_birthdate(form.date_of_birth.data)):
            return 4   
        if not(v.match_pesel_and_birthdate(form.PESEL.data, form.date_of_birth.data)):
            return 5
        if not(v.send_validation_code(form.phone_number.data)):
            return 6
        if not(v.validate_id_data(form.date_of_issue_of_id.data, form.expiry_date_of_id.data, form.place_of_birth.data, form.father_name.data, form.mother_name.data,
                form.id_card_number.data, form.issuing_authority.data, form.nationality.data, form.sex.data)):
            return 7
    
        for i in range(3):
            if v.check_person_via_camera():
                return 0
        return 8

def match_register_error_to_description(error: int) -> str:
    if error == 1:
        return 'Podano niepoprawny email.'
    if error == 2:
        return 'Podane hasła nie sa identyczne.'
    if error == 3:
        return 'Podano niepoprawny PESEL lub plec.'
    if error == 4:
        return 'Podano niepoprawna date urodzenia.'
    if error == 5:
        return 'Data urodzenia i PESEL nie pasują do siebie.'
    if error == 6:
        return 'Blad kodu sms. Sprawdz swoj numer telefonu.'
    if error == 7:
        return 'Niepoprawne dane osobowe na dokumencie.'
    if error == 8:
        return 'Blad weryfikacji twarzy.'

    return 'Cos poszlo nie tak... :(('

def create_new_customer_id() -> str:
    characters = string.ascii_uppercase + string.digits
    for i in range(100):
        random_string = ''.join(random.choice(characters) for _ in range(16))
        if not(customer_id_is_in_database(random_string)):
            return random_string

    raise Exception('Cannot create new login. ??????')

def create_new_transfer_id() -> str:
    characters = string.ascii_uppercase + string.digits
    for i in range(100):
        random_string = ''.join(random.choice(characters) for _ in range(64))
        if not(iban_is_in_database(random_string)):
            return random_string

    raise Exception('Cannot create new transfer id. ??????')

def create_new_employee_id() -> str:
    characters = string.ascii_uppercase + string.digits
    for i in range(100):
        random_string = ''.join(random.choice(characters) for _ in range(16))
        if not(employee_id_is_in_database(random_string)):
            return random_string

    raise Exception('Cannot create new emlpoyee id. ??????')

def create_new_cse_id() -> str:
    characters = string.ascii_uppercase + string.digits
    for i in range(100):
        random_string = ''.join(random.choice(characters) for _ in range(16))
        if not(cse_id_is_in_database(random_string)):
            return random_string

    raise Exception('Cannot create new cse id. ??????')

def send_transfer(dest_iban: str, source_iban: str, title:str, receiver_name:str ,amount: float, customer_id: str):
    customer = Customers.query.filter_by(iban_number=source_iban).first()
    customer.account_balance -= amount
    new_transfer = Transfers(transfer_id=create_new_transfer_id(),sender_iban=source_iban, receiver_iban=dest_iban, 
                             title=title, receiver_name=receiver_name, amount=amount, date=datetime.datetime.now(), sender_id=customer_id)

    db.session.add(new_transfer)
    db.session.commit()
    if iban_is_in_database(dest_iban):
        receiver = Customers.query.filter_by(iban_number=dest_iban).first()
        receiver.account_balance += amount
        db.session.commit()


def beautify_date(list):
    for item in list:
        item.formatted_date  = item.date.strftime("%H:%M %d-%m-%Y")
    return list


def get_transfers(login: str, limit: int, offset: int = 0):
    user = Users.query.filter_by(login=login).first()
    customer = Customers.query.filter_by(pesel=user.pesel).first()
    
    transfers_out = Transfers.query.filter_by(sender_id=customer.customer_id).all()
    transfers_in = Transfers.query.filter_by(receiver_iban=customer.iban_number).all()
    
    transfers = transfers_in + transfers_out
    transfers.sort(key=lambda x: x.date, reverse=True)
    
    recent_transfers = transfers[:offset+limit]
    return beautify_date(recent_transfers)
    
def get_messages(limit: int, offset: int = 0):    
    messages = Messages.query.all()
    messages.sort(key=lambda x: x.date, reverse=False)
    former_messages = messages[:offset+limit]
    return beautify_date(former_messages)



class Transfer_form(FlaskForm):
    amount = StringField(validators=[InputRequired(), Length(min=1)], render_kw={'placeholder': 'Wysokość przelewu'})
    iban_destination = StringField(validators=[InputRequired(), Length(min=28, max=28)], render_kw={'placeholder': 'Nr IBAN konta docelowego'})
    receiver_name = StringField(validators=[InputRequired(), Length(min=1)], render_kw={'placeholder': 'Nazwa odbiorcy'})
    title = StringField(validators=[InputRequired(), Length(min=1)], render_kw={'placeholder': 'Tytul przelewu'})
    submit = SubmitField("Wyslij")


class Login_form(FlaskForm):
    login = StringField(validators=[InputRequired(), Length(min=15, max=15)], render_kw={'placeholder': 'Login'})
    password = PasswordField(validators=[InputRequired(), Length(min=8, max=30)], render_kw={'placeholder': 'Haslo'})
    submit = SubmitField("Login")

class Register_form(FlaskForm):
    first_name = StringField(validators=[InputRequired(), Length(min=2, max=50)], render_kw={'placeholder': 'Imie'})
    last_name = StringField(validators=[InputRequired(), Length(min=2, max=50)], render_kw={'placeholder': 'Nazwisko'})
    PESEL = StringField(validators=[InputRequired(), Length(min=11, max=11)], render_kw={'placeholder': 'PESEL'})
    email = StringField(validators=[InputRequired(), Length(min=2, max=50)], render_kw={'placeholder': 'Email'})
    residence_address = StringField(validators=[InputRequired(), Length(min=2, max=50)], render_kw={'placeholder': 'Adres zamieszkania'})
    phone_number = StringField(validators=[InputRequired(), Length(min=9, max=13)], render_kw={'placeholder': 'Numer telefonu'})
    date_of_birth = StringField(validators=[InputRequired(), Length(min=10, max=10)], render_kw={'placeholder': 'Data urodzenia dd-mm-yyyy'})
    date_of_issue_of_id = StringField(validators=[InputRequired(), Length(min=10, max=10)], render_kw={'placeholder': 'Data wydania dokumentu dd-mm-yyyy'})
    expiry_date_of_id = StringField(validators=[InputRequired(), Length(min=10, max=10)], render_kw={'placeholder': 'Data waznosci dokumentu dd-mm-yyyy'})
    place_of_birth = StringField(validators=[InputRequired(), Length(min=2, max=50)], render_kw={'placeholder': 'Miejsce urodzenia'})
    father_name = StringField(validators=[InputRequired(), Length(min=2, max=50)], render_kw={'placeholder': 'Imie ojca'})
    mother_name = StringField(validators=[InputRequired(), Length(min=2, max=50)], render_kw={'placeholder': 'Imie matki'})
    id_card_number = StringField(validators=[InputRequired(), Length(min=9, max=9)], render_kw={'placeholder': 'Numer dowodu'})
    issuing_authority = StringField(validators=[InputRequired(), Length(min=2, max=50)], render_kw={'placeholder': 'Organ wydający dokument'})
    nationality = StringField(validators=[InputRequired(), Length(min=2, max=50)], render_kw={'placeholder': 'Narodowość'})
    sex = StringField(validators=[InputRequired(), Length(min=1, max=1)], render_kw={'placeholder': 'Plec [M/K]'})
    password = PasswordField(validators=[InputRequired(), Length(min=8, max=30)], render_kw={'placeholder': 'Haslo'})
    repeated_password = PasswordField(validators=[InputRequired(), Length(min=8, max=30)], render_kw={'placeholder': 'Powtorz haslo'})
    submit = SubmitField("Register")