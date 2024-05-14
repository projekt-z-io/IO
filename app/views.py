from app.__init__ import app, db, Customers, Users, PersonalData, bcrypt
from flask import render_template
from app.models.utils import Login_form, Register_form, customer_login, register_customer, create_new_customer_login, create_new_iban
from app.models.tables import  find_max_customer_id

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/index.html")
def index2():
    return render_template('index.html')


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = Login_form()
    return render_template('login.html', form=form)

@app.route("/register",methods=['GET', 'POST'])
def register():
    form = Register_form()
    if form.validate_on_submit():
        if register_customer(form):
            hashed_paswd = bcrypt.generate_password_hash(form.password.data)
            new_user = Users(pesel=form.PESEL.data, first_name=form.first_name.data, last_name=form.last_name.data,login=create_new_customer_login(), email=form.email.data, password=hashed_paswd,phone_number=form.phone_number.data,residence_address=form.residence_address.data, account_active=True)
            db.session.add(new_user)
            db.session.commit()
            customer_id = find_max_customer_id()+1
            new_customer = Customers(customer_id=customer_id, iban_number=create_new_iban(), account_balance=0.0, pesel=form.PESEL.data)
            db.session.add(new_customer)
            db.session.commit()
            new_personal_data = PersonalData(date_of_birth=form.date_of_birth.data, date_of_issue_of_id=form.date_of_issue_of_id.data, expiry_date_of_id=form.expiry_date_of_id.data, place_of_birth=form.place_of_birth.data, father_name=form.father_name.data, mother_name=form.mother_name.data, id_card_number=form.id_card_number.data, issuing_authority=form.issuing_authority.data, nationality=form.nationality.data, sex=form.sex.data, customer_id=customer_id)
            db.session.add(new_personal_data)
            db.session.commit()

    
    return render_template('register.html', form=form)

@app.route("/dashboard")
def dashboard():
    return render_template('dashboard.html')
    