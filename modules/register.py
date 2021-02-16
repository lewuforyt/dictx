import pymongo as mongo
import time
import hashlib
import smtplib
import ssl
from email.mime.text import MIMEText
from modules.entry import *
from modules.config import mongoDbUri


cluster = mongo.MongoClient(mongoDbUri)
db = cluster["sozluk"]
users = db["users"]


def getMailCode():
    code = hashlib.md5(str(time.time())+"tuzum".encode()).hexdigest()

    return code[:7].upper()


def usernameIsTaken(username: str) -> bool:
    allUsers = users.find({})

    for user in allUsers:
        if user["username"] == username:
            return True

    return False


def mailIsTaken(mail: str) -> bool:
    allUsers = users.find({})

    for user in allUsers:
        if user["mail"] == mail:
            return True

    return False


def addUser(username: str, password: str, mail: str, ipAdress: str) -> bool:
    userDict = {
        "username": username,
        "password": password,
        "mail": mail,
        "date": getDate(),
        "mail_activated": False,
        "activation_code": """sendCode(mail)""",
        "roles": ["kayitsiz"],
        "entries": [],
        "loggined_ip_adresses": [ipAdress],
    }

    try:
        users.insert_one(userDict)
        return True
    except:
        return False


# daha sonra belki eklerim
def sendCode(mailAdrr: str):
    code = getMailCode()

    context = ssl.create_default_context()
    smtp_server = "smtp.gmail.com"
    port = 587
    sender_email = ""
    server = smtplib.SMTP(smtp_server, port)
    server.ehlo()
    server.starttls(context=context)
    server.ehlo()
    server.login(sender_email, "")
    text = "<center>sözlüğe hoş geldin! kayıt işlemini başarıyla tamamladın,"
    text += "şimdi ufak bir mail onayı yapman gerekiyor. aşağıda verdiğim linke gidip mail onay kodunu girmen lazım, mail onay kodunu girdiğinde hesabın newbie olarak görünecek. newbie yani acemiler 10 entry girme hakkına sahip. acemiliği başarıyla tamamladıktan sonra yazar olabileceksin. ne duruyorsun, onayla şu hesabı!<br>Kodun: "+code+"</center>"
    mail = MIMEText(text, 'html', 'utf-8')
    mail['From'] = sender_email
    mail['Subject'] = "sözlüğe hoş geldin!"
    mail['To'] = mailAdrr

    mail = mail.as_string()

    server.sendmail(sender_email, mailAdrr, mail)

    return code
