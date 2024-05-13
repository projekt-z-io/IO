import datetime
import re
import random
def validate_pesel(pesel: str, sex: bytes) -> bool:
        if len(pesel) == 11 and pesel.isdigit():
            match int(pesel[9])%2:           # tu pewnie trzeba castowac
                case 0:
                    if sex.lower() == 'k':
                        return check_pesel_control_sum(pesel)
                    return False
                case 1:
                    if sex.lower() == 'm':
                        return check_pesel_control_sum(pesel)
                    return False
        return False

def check_pesel_control_sum(pesel: str) -> bool:
    control_sum =0
    weights = [1, 3, 7, 9, 1, 3, 7, 9, 1, 3]
    for i in range(len(pesel)-1):
        digit = int(pesel[i])
        control_sum  += (digit * weights[i]) % 10
       
    control_sum = (10 - control_sum % 10)

    return control_sum == int(pesel[10])

def validate_birthdate(date_of_birth: str) -> bool:
    currentTime = datetime.datetime.now()
    birthdate = datetime.datetime.strptime(date_of_birth, '%d-%m-%Y')
    if currentTime.year - birthdate.year < 18:
        return False
    return True

def str_to_date(date: str) -> datetime.date:
    return datetime.datetime.strptime(date, '%d-%m-%Y').date()

def pesel_to_birth_date(pesel: str) -> datetime.date:
    year = int(pesel[0:2])
    month = int(pesel[2:4])
    day = int(pesel[4:6])
    
    if month >= 81 and month <= 92:
        year += 1800
        month -= 80
    elif month >= 21 and month <= 32:
        year += 2000
        month -= 20
    elif month >= 41 and month <= 52:
        year += 2100
        month -= 40
    elif month >= 61 and month <= 72:
        year += 2200
        month -= 60
    elif month >= 1 and month <= 12:
        year += 1900
    
    return datetime.date(year, month, day)

def match_pesel_and_birthdate(pesel: str, date_of_birth: str) -> bool:
    birthdate = pesel_to_birth_date(pesel)
    return birthdate == datetime.datetime.strptime(date_of_birth, '%d-%m-%Y').date()

def validate_phone_number(phone_number: str) -> bool:
    if len(phone_number) == 9 and phone_number.isdigit():
        return True
    elif len(phone_number) == 12 and phone_number[0]=='+' and phone_number[1:].isdigit() and phone_number[1:2] == '48':
        return True

    return False
def validate_code(phone_number: str, code: str) -> bool:
        # validating code
    return True

def send_validation_code(phone_number: str) -> bool:
    if validate_phone_number(phone_number):
        code = ''.join(str(random.randint(0, 9)) for _ in range(6))
        # sending code to customers phone number

        return validate_code(phone_number, code)
    return False

def validate_id_data(date_of_issue_of_id: str,
    expiry_date_of_id: str, place_of_birth: str,
    father_name: str, mother_name: str, id_card_number:str,
    issuing_authority: str, nationality: str, sex: bytes) -> bool:
    # checking if id data on photo is valid
    return True

def check_person_via_camera() -> bool:
    return True


def validate_iban(iban) -> bool:

    if not(len(iban) == 28):
        return False
    if not(iban[0:2] == "PL"):
        return False
    
    for i in range(2, 28):
        num = ord(iban[i])
        if not (47 < num < 58):
            return False

    return True


def validate_email(email: str) -> bool:
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if re.match(email_pattern, email):
        return True
    else:
        return False