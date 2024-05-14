import app.models.validators as v
import random
from app.models.tables import iban_is_in_database, login_is_in_database, find_max_customer_id
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
        if i == 99:
            raise Exception('Cannot create new login. ??????')

def register_customer(form) -> bool:

        if not(v.validate_email(form.email.data)):
            return False
        if not(form.password.data == form.repeated_password.data):
            return False
        if not(v.validate_pesel(form.PESEL.data, form.sex.data)):
            return False
        if not(v.validate_birthdate(form.date_of_birth.data)):
            return False   
        if not(v.match_pesel_and_birthdate(form.PESEL.data, form.date_of_birth.data)):
            return False
        if not(v.send_validation_code(form.phone_number.data)):
            return False
        if not(v.validate_id_data(form.date_of_issue_of_id.data, form.expiry_date_of_id.data, form.place_of_birth.data, form.father_name.data, form.mother_name.data,
                form.id_card_number.data, form.issuing_authority.data, form.nationality.data, form.sex.data)):
            return False
    
        for i in range(3):
            if v.check_person_via_camera():
                return True
        return False

def create_new_customer_id(max_) -> str:
    return str(max_+1)

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
    date_of_birth = StringField(validators=[InputRequired(), Length(min=10, max=10)], render_kw={'placeholder': 'Data urodzenia'})
    date_of_issue_of_id = StringField(validators=[InputRequired(), Length(min=10, max=10)], render_kw={'placeholder': 'Data wydania dokumentu'})
    expiry_date_of_id = StringField(validators=[InputRequired(), Length(min=10, max=10)], render_kw={'placeholder': 'Data waznosci dokumentu'})
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