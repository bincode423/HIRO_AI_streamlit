import smtplib
import re
import pickle
from email.mime.text import MIMEText

my_email = None
password = None

def send_email(send_e_mail, html):
    smtp = smtplib.SMTP('smtp.gmail.com', 587)
    smtp.ehlo()
    smtp.starttls()
    smtp.login(my_email, password)
    
    msg = MIMEText(html, "html", "utf-8")
    msg['Subject'] = "HIRO AI"
    msg['From'] = my_email
    msg['To'] = send_e_mail
    smtp.sendmail(my_email, send_e_mail, msg.as_string())
    smtp.quit()

def send_code_email(send_e_mail, code, name):
    with open("./document/html/email_code.html", "r", encoding="utf-8") as f:
        html = f.read()
    html = html.replace("[사용자 이름]", name)
    html = html.replace("[여기에 6자리 숫자 또는 문자열 인증 코드 삽입]", code)
    send_email(send_e_mail, html)

def check_email(email):
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(pattern, email) is not None

def copy_email(email):
    try:
        with open('./database/email.pkl', 'rb') as f:
            emails = pickle.load(f)
    except FileNotFoundError:
        emails = set()
    return email not in emails

def add_email(email):
    with open('./database/email.pkl', "rb") as f:
        email_list = pickle.load(f)
    if email in email_list:
        print(f"Email '{email}' is already in the list.")
        return False
    email_list.add(email)
    with open('./database/email.pkl', "wb") as f:
        pickle.dump(email_list, f)

    print(f"Email '{email}' added successfully.")