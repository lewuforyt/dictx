import pymongo as mongo
import hashlib
import datetime
import re
from modules.lasts import *
from modules.index import *
from modules.report import *
from modules.config import mongoDbUri


cluster = mongo.MongoClient(mongoDbUri)
db = cluster["sozluk"]
entries = db["entries"]
users = db["users"]
baslik = db["basliklar"]
reps = db["reports"]


def getBaslikFromName(baslikAdi: str):
    basliklarr = baslik.find({"baslik": baslikAdi})
    adi = None
    for i in basliklarr:
        adi = i

    return adi


def entryBeautifier(message: str):
    messageA = message.replace("<", "&lt;").replace(">", "&gt;").replace("\n", "<br>")
    bulundu = re.findall("\(bkz: ([A-Za-z0-9 üğçöıuş]+\))", message)
    for i in bulundu:
        i = i.replace(")", "")

        if getBaslikFromName(i):
            print(f"(bkz: {i})")
            print(f'(bkz: <a href="/baslik/{getBaslikFromName(i)["baslikId"]}">{i}</a>)')
            messageA = messageA.replace(f"(bkz: {i})", f'(bkz: <a href="/baslik/{getBaslikFromName(i)["baslikId"]}">{i}</a>)')

    return messageA


def reportBul(id):
    bul = reps.find({"reportId": int(id)})

    i = None
    for _ in bul:
        i = _

    return i


def editEntry(username: str, password: str, entryId: str, message: str):

    entry = entryBul(entryId)

    if isLoggedIn(username, password):
        if entry["author"] == username or isAdmin(username, password):
            entries.update_one({"entryId": int(entryId)}, {"$set": {"message": message}})

            return True

    return False


def isLoggedIn(username: str, password: str):
    allUsers = users.find({})

    for user in allUsers:
        if user["username"] == username:
            if createMd5Password(user["password"]) == password:
                return True

    return False


def entryBul(id):
    bul = entries.find({"entryId": int(id)})

    i = None
    for _ in bul:

        i = _

    return i


def getDate():
    an = datetime.datetime.now()
    fark = datetime.timedelta(hours=3)
    an = an+fark
    date = str(an.day)+"."+str(an.month)+"."+str(an.year)+" "+str(an.hour)+":"+str(an.minute)

    return date


def addBaslik(username: str, password: str, baslikAdi: str):
    lEntry, lBaslik, lReport = getLasts()

    newBaslik = {
        "author": username,
        "baslik": baslikAdi.lower(),
        "baslikId": lBaslik+1,
        "date": getDate(),
        "follows": []
    }

    if isLoggedIn(username, password):
        baslik.insert_one(newBaslik)
        return newBaslik

    return False


def addEntry(username: str, password: str, message: str, baslikId: int):
    lEntry, lBaslik, lReport = getLasts()

    allBasliklar = baslik.find({})

    resultBaslik = None
    for basliki in allBasliklar:
        if basliki["baslikId"] == int(baslikId):
            resultBaslik = basliki["baslik"]

    if not baslik:
        return False

    newEntry = {
        "author": username,
        "entryId": lEntry+1,
        "message": message.lower(),
        "baslik": resultBaslik,
        "baslikId": int(baslikId),
        "date": getDate(),
        "likes": []
    }

    if isLoggedIn(username, password):
        entries.insert_one(newEntry)
        return newEntry

    return False


def baslikFromId(id):
    allBaslik = baslik.find({"baslikId": id})
    thisBaslik = None
    for basliki in allBaslik:
        thisBaslik = basliki["baslik"]

    return thisBaslik


def getMessagesFromBaslikId(id: int):
    allEntries = entries.find({"baslikId": int(id)})

    result = []

    for entry in allEntries:
        result.append(entry)

    return result


def deleteEntry(username, password, entryId):

    if isLoggedIn(username, password):
        entr = entryBul(int(entryId))

        if entr["author"] == username or isAdmin(username, password):
            entries.delete_one({"entryId": int(entryId)})
            return True

    return False


def deleteReportFunc(username, password, reportId):
    if isLoggedIn(username, password):
        entr = reportBul(int(reportId))
        if entr["username"] == username or isAdmin(username, password):
            reports.delete_one({"reportId": int(reportId)})
            return True

    return False


def baslikVarMi(baslikAdi):
    tumu = baslik.find({"baslik": baslikAdi})

    i = None
    for baslikk in tumu:
        i = baslikk

    return i
