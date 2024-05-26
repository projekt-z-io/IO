from app.__init__ import app, db, Customers, Users, PersonalData,CustomerServiceEmployees, Admins, bcrypt, Employees, Messages
from flask import render_template, redirect, url_for, request
from app.models.utils import Login_form, Register_form, Transfer_form,create_new_cse_id,create_new_employee_id, get_messages ,get_transfers, send_transfer, register_customer, create_new_login, create_new_iban, create_new_customer_id, match_register_error_to_description
from flask_login import login_user, LoginManager, logout_user, login_required, current_user
from app.models.validators import str_to_date, validate_transfer
import datetime
from app.models.tables import user_is_employee

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
        if user_is_employee(form.login.data):
            return redirect(url_for('employee_login'))
        user = Users.query.filter_by(login=form.login.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('dashboard'))

    return render_template('login.html', form=form)


@app.route("/dashboard", methods=['GET','POST'])
@login_required
def dashboard():
    balance = Customers.query.filter_by(pesel=current_user.pesel).first().account_balance
    return render_template('dashboard.html', balance=balance)

@app.route("/logout", methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route("/register",methods=['GET', 'POST'])
def register():
    error = 0
    form = Register_form()
    if form.validate_on_submit():
        error = register_customer(form)
        if error == 0:
            hashed_paswd = bcrypt.generate_password_hash(form.password.data)
            login=create_new_login()
            new_user = Users(pesel=form.PESEL.data, first_name=form.first_name.data, last_name=form.last_name.data,login=login, email=form.email.data, password=hashed_paswd,phone_number=form.phone_number.data,residence_address=form.residence_address.data, account_active=True)
            db.session.add(new_user)
            db.session.commit()
            customer_id = create_new_customer_id()
            new_customer = Customers(customer_id=customer_id, iban_number=create_new_iban(), account_balance=0.0, pesel=form.PESEL.data)
            db.session.add(new_customer)
            db.session.commit()
            new_personal_data = PersonalData(date_of_birth=str_to_date(form.date_of_birth.data), date_of_issue_of_id=str_to_date(form.date_of_issue_of_id.data), expiry_date_of_id=str_to_date(form.expiry_date_of_id.data), place_of_birth=form.place_of_birth.data, father_name=form.father_name.data, mother_name=form.mother_name.data, id_card_number=form.id_card_number.data, issuing_authority=form.issuing_authority.data, nationality=form.nationality.data, sex=form.sex.data, customer_id=customer_id)
            db.session.add(new_personal_data)
            db.session.commit()
            return redirect(url_for('welcome', login=login))


    return render_template('register.html', form=form, error=error, error_desc=match_register_error_to_description(error))

@app.route("/welcome", methods=['GET','POST'])
def welcome():
    login = request.args.get('login')
    return render_template('welcome.html', login=login)

@app.route("/employee_login", methods=['GET','POST'])
def employee_login():
    form = Login_form()
    if form.validate_on_submit():
        user = Users.query.filter_by(login=form.login.data).first()
        employee = Employees.query.filter_by(pesel=user.pesel).first()
        if not(employee):
            return render_template('employee_login.html')
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                
                cse = CustomerServiceEmployees.query.filter_by(employee_id=employee.employee_id).first()
                if cse:
                    login_user(user)
                    return redirect(url_for('cse_dashboard'))
                
                admin = Admins.query.filter_by(employee_id=employee.employee_id).first()
                
                if admin:
                    login_user(user)
                    return redirect(url_for('admin_dashboard'))

    return render_template('employee_login.html', form=form)

@app.route("/cse_dashboard", methods=['GET','POST'])
@login_required
def cse_dashboard():
    limit = 10
    offset = int(request.args.get('offset', 0))
    messages = get_messages(limit, offset)
    return render_template("cse_dashboard.html",messages=messages, offset=offset, limit=limit)

@app.route("/admin_dashboard", methods=['GET','POST'])
@login_required 
def admin_dashboard():
    return render_template('admin_dashboard.html')

@app.route("/make_transfer", methods=['GET', 'POST'])
@login_required
def make_transfer():
    login = current_user.login
    user = Users.query.filter_by(login=login).first()
    customer = Customers.query.filter_by(pesel=user.pesel).first()
    form = Transfer_form()
    if form.validate_on_submit():
        amount = form.amount.data
        dest_iban = form.iban_destination.data
        ok, amount_float = validate_transfer(dest_iban=dest_iban, amount=amount, customer_balance=customer.account_balance)
        if ok:
            send_transfer(dest_iban=dest_iban, source_iban=customer.iban_number, title=form.title.data,
                           receiver_name=form.receiver_name.data, amount=amount_float, customer_id=customer.customer_id)
            return render_template("transfer_made.html", dest_iban=dest_iban, amount=amount_float, current_balance=customer.account_balance)

    return render_template("make_transfer.html",form=form, iban_source=customer.iban_number, balance=customer.account_balance)
    
@app.route("/transfer_history", methods=['GET','POST'])
@login_required
def transfer_history():
    limit = 10
    offset = int(request.args.get('offset', 0))
    transfers = get_transfers(current_user.login, limit, offset)
    pesel = current_user.pesel
    customer_id = Customers.query.filter_by(pesel=pesel).first().customer_id
    return render_template("transfer_history.html", transfers=transfers, current_customer_id=customer_id, offset=offset, limit=limit)