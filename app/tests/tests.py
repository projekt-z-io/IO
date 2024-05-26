# def test(amount):
#     Customers.query.filter_by(pesel='59052624515').first().account_balance += amount
# def test_cse():
#     login=create_new_login()
#     hashed_paswd = bcrypt.generate_password_hash("test1234")
#     new_user = Users(pesel='89042951266', first_name="test3", last_name="test3",login=login, email="test3@test.com", password=hashed_paswd,phone_number="123456789",residence_address="Ustka", account_active=True)
#     db.session.add(new_user)
#     db.session.commit()
#     em_id = create_new_employee_id()
#     new_employee = Employees(pesel='89042951266', salary=1000, room="1", office="1", shift=1, employee_id=em_id)
#     db.session.add(new_employee)
#     db.session.commit()
#     new_cse = CustomerServiceEmployees(employee_id="SAG2PYA41RED5SRG", cse_id=create_new_cse_id())
#     db.session.add(new_cse)
#     db.session.commit()

# def test_messages():
#     for i in range(0, 13):
#         message = Messages(message_id=create_new_cse_id(),
#                            content=f"test{i}",
#                            date=datetime.datetime.now(),customer_id="XDK5LNVX79RUSC3Y",cse_id="3OCM27UC5GAZX887")
#         db.session.add(message)

#     db.session.commit()


# def test_remove_cse():
#     CustomerServiceEmployees.query.filter_by(cse_id="U7SOJ3T5DUX91K0M").delete()
#     db.session.commit()



# def test_admin():
#     login=create_new_login()
#     hashed_paswd = bcrypt.generate_password_hash("test1234")
#     new_user = Users(pesel='63071556892', first_name="test4", last_name="test4",login=login, email="test4@test.com", password=hashed_paswd,phone_number="123451789",residence_address="Ustka", account_active=True)
#     db.session.add(new_user)
#     db.session.commit()
#     em_id = create_new_employee_id()
#     new_employee = Employees(pesel='63071556892', salary=1000, room="2", office="2", shift=3, employee_id=em_id)
#     db.session.add(new_employee)
#     db.session.commit()
#     new_admin = Admins(employee_id=em_id, admin_id=create_new_admin_id())
#     db.session.add(new_admin)
#     db.session.commit()