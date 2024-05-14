from app.__init__ import app, db, Customers, Users, PersonalData, bcrypt
from flask import render_template, redirect, url_for, request
from app.models.utils import Login_form, Register_form, register_customer, create_new_login, create_new_iban
from app.models.tables import  find_max_customer_id
from flask_login import login_user, LoginManager, logout_user, login_required, current_user


login_manager = LoginManager()
login_manager.init_app(app)


login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(pesel):
    return Users.query.get(pesel)


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = Login_form()
    if form.validate_on_submit():
        user = Users.query.filter_by(login=form.login.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('dashboard'))

    return render_template('login.html', form=form)


@app.route("/dashboard", methods=['GET','POST'])
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route("/logout", methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route("/register",methods=['GET', 'POST'])
def register():
    form = Register_form()
    if form.validate_on_submit():
        if register_customer(form):
            hashed_paswd = bcrypt.generate_password_hash(form.password.data)
            new_user = Users(pesel=form.PESEL.data, first_name=form.first_name.data, last_name=form.last_name.data,login=create_new_login(), email=form.email.data, password=hashed_paswd,phone_number=form.phone_number.data,residence_address=form.residence_address.data, account_active=True)
            db.session.add(new_user)
            db.session.commit()
            customer_id = find_max_customer_id()+1
            new_customer = Customers(customer_id=customer_id, iban_number=create_new_iban(), account_balance=0.0, pesel=form.PESEL.data)
            db.session.add(new_customer)
            db.session.commit()                         # tu cos nie działa
            new_personal_data = PersonalData(date_of_birth=form.date_of_birth.data, date_of_issue_of_id=form.date_of_issue_of_id.data, expiry_date_of_id=form.expiry_date_of_id.data, place_of_birth=form.place_of_birth.data, father_name=form.father_name.data, mother_name=form.mother_name.data, id_card_number=form.id_card_number.data, issuing_authority=form.issuing_authority.data, nationality=form.nationality.data, sex=form.sex.data, customer_id=customer_id)
            db.session.add(new_personal_data)
            db.session.commit()                         # tu tez
            return redirect(url_for('login'))           # to do ekran powitalny

    
    return render_template('register.html', form=form)


