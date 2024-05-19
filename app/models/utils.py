import app.models.validators as v
import random
from app.models.tables import iban_is_in_database, login_is_in_database, customer_id_is_in_database
#from flask_login import UserMixin
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from app.__init__ import bcrypt 
import string

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