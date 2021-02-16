import pymongo as mongo
from modules.config import mongoDbUri


cluster = mongo.MongoClient(mongoDbUri)
db = cluster["sozluk"]
entries = db["entries"]
users = db["users"]


def get5EntryFromUsername(username: str) -> list:
    tum_entryleri = entries.find({"author": username})
    tum = []

    for i in tum_entryleri:
        tum.append(i)

    tum.reverse()
    return tum[:5]


def userControl(username: str):
    us = users.find({"username": username})

    name = None
    for _ in us:
        name = _

    return name


def userEntryCount(username: str) -> int:
    allEntryyy = entries.find({"author": username})

    ent = []

    for i in allEntryyy:
        ent.append(i)

    return len(ent)
