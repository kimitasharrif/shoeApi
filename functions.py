# Send SMS
# africatalking-sending sms
#bcrypt-data encryption cyber security
#flask- creating a server
#request- mpesa server communication
#flask_restiful-
#fpdf-generating pdf
# pymysql- connecting database
# cryptography
import africastalking
africastalking.initialize(
   username="joe2022",
   api_key="aab3047eb9ccfb3973f928d4ebdead@@__9e60beb936b4d2838f7725c9cc165f0c8a"
   # justpaste.it/1nua8   
)

sms = africastalking.SMS
def send_sms(phone, message):
    recipients = [phone]
    sender = "AFRICASTKNG"
    try:
        response = sms.send(message, recipients)
        print(response)
    except Exception as error:
        print("Error is ", error)


#send_sms("+254729225710", "This is test message on Fleet.")

def gen_random(N):
    import string
    import random
    
    # using random.choices()
    # generating random strings
    res = ''.join(random.choices(string.digits + string.ascii_lowercase, k=N))
    # print result
    print("The generated random string : " + str(res))
    return str(res)
    
# Test    
# gen_random(N=6)

import bcrypt
def hash_password(password):
    bytes = password.encode("utf-8")
    salt = bcrypt.gensalt()
    print('Salt: ', salt)
    hash = bcrypt.hashpw(bytes, salt)
    print("Hash", hash.decode())
    return hash.decode()

#TEST
#hash_password("Nairobi40")
#$2b$12$QZIOoEiOfHYq6PjT5g8WUOKe53nnozlhfL/9iEmj9R3k1tQVaoU9.

def hash_verify(password,  hashed_password):
    bytes = password.encode('utf-8')
    result = bcrypt.checkpw(bytes, hashed_password.encode())
    print(result)
    return result


#hash_verify("Nairobi40", "$2b$12$QZIOoEiOfHYq6PjT5g8WUOKe53nnozlhfL/9iEmj9R3k1tQVaoU9.")
# AES, RSA

# generates Encryption Key
from cryptography.fernet import  Fernet
def gen_key():
    key = Fernet.generate_key()
    with open("key.key", "wb") as key_file:
        key_file.write(key)
# Test
# gen_key()

def load_key():
    return open("key.key", "rb").read()

def encrypt(data):
    key = load_key()
    f = Fernet(key)
    encrypted_data = f.encrypt(data.encode())
    print("Plain ", data)
    print("Encrypted ", encrypted_data.decode())
    return encrypted_data.decode()
# Test
# encrypt("+25472922vfyfufhb")
#gAAAAABmr6PGfjpzEw114ovkHV4LB5NiF0XKayfpFMlN8OOSVdAsoFx46sMZJTwrv9G9WOyc0UybKSwE83y2tmcCruEIZzzes5aR2aHx0PqQXH4FV8SgAhA=

def decrypt(encrypted_data):
    key = load_key()
    f = Fernet(key)
    decrypted_data = f.decrypt(encrypted_data.encode())
    print("Decrypted data ", decrypted_data.decode())
    return decrypted_data.decode()
# Test - Provide the Encrypted
# decrypt("gAAAAABmr6PGfjpzEw114ovkHV4LB5NiF0XKayfpFMlN8OOSVdAsoFx46sMZJTwrv9G9WOyc0UybKSwE83y2tmcCruEIZzzes5aR2aHx0PqQXH4FV8SgAhA=")
# Symetric and Asymetric Encryption
# Asymetric Encryption - Research using Python. 
# Pending ******
def send_email(email, message):
    import smtplib
    # creates SMTP session
    s = smtplib.SMTP('smtp.gmail.com', 587)
    # start TLS for security
    s.starttls()
    # Authentication
    s.login("modcomlearning2@gmail.com", "")
    # sending the mail
    s.sendmail("modcomlearning@gmail.com", email, message)
    # terminating the session
    s.quit()
    
# Test
#send_email("johndoe@gmail.com", "Test Email")
import requests
import base64
import datetime
from requests.auth import HTTPBasicAuth

# In this fucntion we provide phone(used to pay), amount to be paid and invoice no being paid for.
def mpesa_payment(amount, phone, invoice_no):
        # GENERATING THE ACCESS TOKEN
        consumer_key = "oAN7tFvWXa4qJ6XWAqcjG3RZoMGsSOXA"
        consumer_secret = "J2TFUVbsnM5CEvvr"

        api_URL = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"  # AUTH URL
        r = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))

        data = r.json()
        access_token = "Bearer" + ' ' + data['access_token']
        print(access_token)

        #  GETTING THE PASSWORD
        timestamp = datetime.datetime.today().strftime('%Y%m%d%H%M%S')
        passkey = 'bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919'
        business_short_code = "174379"
        data = business_short_code + passkey + timestamp
        encoded = base64.b64encode(data.encode())
        password = encoded.decode('utf-8')
        print(password)

        # BODY OR PAYLOAD
        payload = {
            "BusinessShortCode": "174379",
            "Password": "{}".format(password),
            "Timestamp": "{}".format(timestamp),
            "TransactionType": "CustomerPayBillOnline",
            "Amount": amount,  # use 1 when testing
            "PartyA": phone,  # change to your number
            "PartyB": "174379",
            "PhoneNumber": phone,
            "CallBackURL": "https://modcom.co.ke/job/confirmation.php",
            "AccountReference": "Lab Account",
            "TransactionDesc": "account"
        }

        # POPULAING THE HTTP HEADER
        headers = {
            "Authorization": access_token,
            "Content-Type": "application/json"
        }

        url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"  # C2B URL

        response = requests.post(url, json=payload, headers=headers)
        print(response.text)
# Test
# mpesa_payment("2", "254729225710", "NCV003")

def gen_pdf():
    # Python program to create
    # a pdf file
    from fpdf import FPDF
    # save FPDF() class into a
    # variable pdf
    pdf = FPDF()
    # Add a page
    pdf.add_page()
    # set style and size of font
    # that you want in the pdf
    pdf.set_font("Arial", size=15)
    # create a cell
    pdf.cell(200, 10, txt="ModcomInstitute of tech",
             ln=1, align='L')
    # add another cell
    pdf.cell(200, 10, txt="A Computer Science portal for geeks.",
             ln=2, align='C')
    
    pdf.cell(200, 10, txt="Welcome.",
             ln=2, align='C')
    # save the pdf with name .pdf
    pdf.output("cv.pdf")

# Test
#gen_pdf()
import re
def passwordValidity(password):
    if(len(password) < 8):
        return "Your Password Must be greater than 8"
    
    elif not re.search("[a-z]", password):
        return "You must have at least a small letter"
    
    elif not re.search("[A-Z]", password):
        return "You must have at least a Capital letter"
    
    elif not re.search("[0-9]", password):
        return "You must have at least a Number"
    
    elif not re.search("[a-z]", password):
        return "You must have at least a small letter"

    elif not re.search("[@#$%^&!?]", password):
        return "You must have at least a symbol" 
    
    else:
        return True
# Test
# x = passwordValidity("Ajkgh14gh")
# print(x)
import re
def normalize_phone(phone):
    if phone.startswith("+254"):
        return phone
    elif phone.startswith("254"):
        return "+" + phone
    elif phone.startswith("07"):
        return "+254" + phone[1:]
    elif phone.startswith("011") and len(phone) == 10:
        return "+254" + phone[1:]
    else:
        return phone
    
def check_phone(phone):
    normalized_phone = normalize_phone(phone)
    print("Normalized phone:", normalized_phone)
    
    # Define regex pattern for the normalized phone format
    pattern = r"^\+254\d{9}$"
    
    # Check if the normalized phone matches the pattern
    if re.match(pattern, normalized_phone):
        print("Phone Ok")
        return True
    
    # If no pattern matches
    print("Phone Not Ok")
    return False   

# Example usage:
# print(check_phone("+254712345678"))  # Phone Ok
# print(check_phone("254712345678"))   # Phone Ok
# print(check_phone("0712345678"))     # Phone Ok
# print(check_phone("712345678"))      # Phone Not Ok
# print(check_phone("0112345676"))   # Phone Ok
# print(check_phone("0172345678"))  # Phone Ok/not
# print(check_phone("0823345678"))   # Phone not Ok
# print(check_phone("0612345678"))     # Phone not ok