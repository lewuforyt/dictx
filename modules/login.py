import pymongo as mongo
import hashlib
import datetime
from modules.config import mongoDbUri


cluster = mongo.MongoClient(mongoDbUri)
db = cluster["sozluk"]
users = db["users"]


def createMd5Password(password: str) -> str:
    passwd = hashlib.md5(str(password+password[-1:-3]+"a788s").encode()).hexdigest()

    return passwd


def LoginProccess(unameOrMail: str, password: str, ipAddr: str):
    allUsers = users.find({})
    for user in allUsers:
        if user["username"] == unameOrMail or user["mail"] == unameOrMail:
            ipList = user["loggined_ip_adresses"]
            ipList.append(ipAddr)

            users.update_one({"username": user["username"]}, {"$set": {"loggined_ip_adresses": ipList}})
            return True, user["username"]

    return False, False
