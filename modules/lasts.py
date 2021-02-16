import pymongo as mongo
import datetime
from modules.config import mongoDbUri


cluster = mongo.MongoClient(mongoDbUri)
db = cluster["sozluk"]
lasts = db["last"]

basliks = db["basliklar"]
entries = db["entries"]
reports = db["reports"]

lastent = db["lastentries"]


def getLasts():
    entry = 0
    baslik = 0
    report = 0

    allBaslik = basliks.find({}).sort("baslikId", mongo.ASCENDING)

    for _ in allBaslik:
        baslik = _["baslikId"]

    allEntry = entries.find({}).sort("entryId", mongo.ASCENDING)

    for _ in allEntry:
        entry = _["entryId"]

    allReport = entries.find({}).sort("reportId", mongo.ASCENDING)

    for _ in allReport:
        report = _["entryId"]

    return entry, baslik, report


def addNewLastEntry(username):
    new = {
        "username": username,
        "expire_at": datetime.datetime.now() + datetime.timedelta(minutes=1)
    }

    lastent.create_index("expire_at", expireAfterSeconds=1)
    lastent.insert_one(new)
