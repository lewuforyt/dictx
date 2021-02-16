import pymongo as mongo
import hashlib
from modules.login import *
from modules.entry import *
from modules.config import mongoDbUri


cluster = mongo.MongoClient(mongoDbUri)
db = cluster["sozluk"]
users = db["users"]
basliklar = db["basliklar"]


def isLoggedIn(username: str, password: str):
    allUsers = users.find({})
    print(username, password)
    for user in allUsers:
        if user["username"] == username:
            print("usererere")
            if createMd5Password(user["password"]) == password:
                return True

    return False


def getMessagesFromBaslikId(id: int):
    allEntries = entries.find({"baslikId": int(id)})

    result = []

    for entry in allEntries:
        result.append(entry)

    return result


def gundemBasliklar():
    allBaslik = basliklar.find({})

    basliks = []
    for i in allBaslik:
        new = {
            "baslik": i["baslik"],
            "baslikId": i["baslikId"],
            "postlar": len(getMessagesFromBaslikId(i["baslikId"])),
        }
        basliks.append(new)

    return basliks
