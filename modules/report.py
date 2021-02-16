import pymongo as mongo
from modules.index import *
from modules.lasts import *
from modules.entry import *
from modules.config import mongoDbUri


cluster = mongo.MongoClient(mongoDbUri)
db = cluster["sozluk"]
reports = db["reports"]
users = db["users"]


def getDate():
    an = datetime.datetime.now()
    fark = datetime.timedelta(hours=3)
    an = an+fark
    date = str(an.day)+"."+str(an.month)+"."+str(an.year)+" "+str(int(an.hour)+3)+":"+str(an.minute)

    return date


def isLoggedIn(username: str, password: str):
    allUsers = users.find({})

    for user in allUsers:
        if user["username"] == username:
            if createMd5Password(user["password"]) == password:
                return True

    return False


def isAdmin(username: str, password: str):

    if isLoggedIn(username, password):
        for _ in users.find({"username": username}):

            if "admin" in _["roles"]:
                return True

    return False


def getReports():
    allReports = reports.find({})

    result = []
    for _ in allReports:
        result.append(_)

    return result


def addReport(username: str, password: str, entryId: int, reason: str):
    lEntry, lBaslik, lReport = getLasts()
    new = {
        "username": username,
        "entryId": int(entryId),
        "reason": reason,
        "date": getDate(),
        "reportId": lReport+1
    }
    print(new)

    if isLoggedIn(username, password):
        reports.insert_one(new)
        return True

    return False
