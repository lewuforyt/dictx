from flask import Flask, request, make_response, redirect
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask import render_template
import requests
from modules.register import *
from modules.login import *
from modules.index import *
from modules.report import *
from modules.profile import *
from modules.lasts import getLasts
from modules.entry import *
from modules.config import secretKey


app = Flask(__name__)

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)


@app.route("/dev/<username>")
def profil(username):

    if userControl(username):
        entryc = userEntryCount(username)
        return render_template("profil.html", entryc=entryc, user=userControl(username), result=get5EntryFromUsername(username), gundemBasliklar=gundemBasliklar(), logged_in=isLoggedIn(request.cookies.get("username"), request.cookies.get("password")))
    return "asdas"


def getIp(request):
    try:
        if request.environ['HTTP_X_FORWARDED_FOR']:
            return request.environ['HTTP_X_FORWARDED_FOR']
    except:
        return request.environ['REMOTE_ADDR']


def kontrol(key):
    r = requests.get(f"https://www.google.com/recaptcha/api/siteverify?secret={secretKey}&response="+key).json()

    return r["success"]


@app.route('/giris', methods=["POST", "GET"])
def login():
    loggedIn = isLoggedIn(request.cookies.get("username"), request.cookies.get("password"))
    if loggedIn:
        return redirect("/")

    if request.method == "POST":
        if kontrol(request.form.get("g-recaptcha-response")):
            username = request.form.get("username")
            password = request.form.get("password")

            result, uname = LoginProccess(username, password, getIp(request))
            print(result, uname)
            if result:
                response = make_response(redirect("/"))
                response.set_cookie("username", uname)
                response.set_cookie("password", createMd5Password(password))

                return response
            else:
                return "böyle bir kullanıcımız yok. belki vardır da şifreni yanlış yazmışsındır"
        else:
            return "recaptcha yanlıştı"

    return render_template("login.html")


@app.route("/kayit", methods=["GET", "POST"])
def register():
    loggedIn = isLoggedIn(request.cookies.get("username"), request.cookies.get("password"))
    if loggedIn:
        return redirect("/")
    if request.method == "POST":
        username = request.form.get("username")
        mail = request.form.get("mail")
        password = request.form.get("password")

        if kontrol(request.form.get("g-recaptcha-response")):
            if not usernameIsTaken(username):
                if not mailIsTaken(mail):
                    addUser(username, password, mail, getIp(request))
                    return redirect("/giris")
                else:
                    return "mail alınmış"
            else:
                return "kullanıcı adı alınmış"
        else:
            return "recaptcha doldurulmadı"

    return render_template("register.html")


@app.route("/", methods=["GET"])
def index():

    logged_in = isLoggedIn(request.cookies.get("username"), request.cookies.get("password"))
    gundemBasliklarim = gundemBasliklar()

    gundementryler = getMessagesFromBaslikId(gundemBasliklarim[0]["baslikId"])
    return render_template("index.html", logged_in=logged_in, result=gundementryler, a=gundemBasliklarim[0], entryBeautifier=entryBeautifier, gundemBasliklar=gundemBasliklar())


@app.route("/baslik/<id>", methods=["GET"])
def baslik(id):
    admin_mi = isAdmin(request.cookies.get("username"), request.cookies.get("password"))
    logged_in = isLoggedIn(request.cookies.get("username"), request.cookies.get("password"))
    baslikAdi = baslikFromId(int(id))
    page = request.args.get("p")

    if baslikAdi:
        resultOne = getMessagesFromBaslikId(int(id))
        if page:
            page = int(page)

            result = resultOne[(page-1)*10:page*10]

        if not page:
            result = resultOne[:10]

        return render_template("baslik.html", entryBeautifier=entryBeautifier, baslikAdi=baslikAdi, logged_in=logged_in, admin_mi=admin_mi, result=result, baslikId=id, loop=int(len(resultOne)/10)+1, gundemBasliklar=gundemBasliklar())

    return render_template("baslik.html", logged_in=logged_in, baslikAdi="", baslikId=id, admin_mi=admin_mi)


@app.route("/entry/<id>", methods=["GET"])
def entry(id):
    if request.method == "GET":
        username, passwd = request.cookies.get("username"), request.cookies.get("password")
        logged_in = isLoggedIn(username, passwd)

        entry = entryBul(int(id))

        return render_template("entry.html", logged_in=logged_in, entry=entry, gundemBasliklar=gundemBasliklar(), entryBeautifier=entryBeautifier, admin_mi=isAdmin(username, passwd))


@limiter.limit("12 per hour")
@app.route("/ekle", methods=["POST"])
def ekle():
    if request.method == "POST":
        username = request.cookies.get("username")
        password = request.cookies.get("password")
        message = request.form.get("message")
        baslikId = request.form.get("baslikId")

        if getMessagesFromBaslikId(baslikId) == []:
            return ":D"

        result = addEntry(username, password, message, baslikId)
        return "ok"

        if not result:
            return "bir şeyler yanlış gitti :/"


@limiter.limit("3 per hour")
@app.route("/yenibaslik", methods=["POST"])
def baslikEkle():
    logged_in = isLoggedIn(request.cookies.get("username"), request.cookies.get("password"))

    if request.method == "POST":
        baslikAdi = request.form.get("baslik-adi")
        ilkMesaj = request.form.get("message")

        if len(baslikAdi) > 150:
            return "başlık çok uzun"

        if baslikVarMi(baslikAdi):
            addEntry(request.cookies.get("username"), request.cookies.get("password"), ilkMesaj, baslikVarMi(baslikAdi)["baslikId"])
            return redirect("/baslik/"+str(baslikVarMi(baslikAdi)["baslikId"]))

        basliki = addBaslik(request.cookies.get("username"), request.cookies.get("password"), baslikAdi)["baslikId"]
        eklenen = addEntry(request.cookies.get("username"), request.cookies.get("password"), ilkMesaj, basliki)

        return redirect("/baslik/"+str(basliki))


@app.route("/cikis", methods=["GET"])
def cikisSayfasi():
    resp = make_response(redirect("/"))
    resp.set_cookie("password", "")
    resp.set_cookie("username", "")

    return resp


@app.route("/yenibaslik", methods=["GET"])
def baslikeklesayfasi():
    logged_in = isLoggedIn(request.cookies.get("username"), request.cookies.get("password"))
    return render_template("yenibaslik.html", logged_in=logged_in, gundemBasliklar=gundemBasliklar())


@app.route("/report/<id>", methods=["GET", "POST"])
def reportMessage(id):
    if request.method == "POST":
        username = request.cookies.get("username")
        password = request.cookies.get("password")
        reason = request.form.get("reason")
        entryId = request.form.get("entryId")
        s = addReport(username, password, entryId,  reason)

        return redirect("/entry/"+id)

    if not isLoggedIn(request.cookies.get("username"), request.cookies.get("password")):
        return redirect("/entry/"+id)

    entry = entryBul(int(id))
    print(entry)
    logged_in = isLoggedIn(request.cookies.get("username"), request.cookies.get("password"))
    return render_template("report.html", entry=entry, logged_in=logged_in)


@app.route("/reports", methods=["GET"])
def reports():

    if not isAdmin(request.cookies.get("username"), request.cookies.get("password")):
        return redirect("/")
    return render_template("reports.html", result=getReports())


@app.route("/deleteMessage", methods=["POST"])
def deleteMessage():

    if request.method == "POST":
        username = request.cookies.get("username")
        password = request.cookies.get("password")
        entryId = request.form.get("entryId")

        s = deleteEntry(username, password, entryId)

        return "ok"

    return "permission error"


@app.route("/deleteReport", methods=["POST"])
def deleteReport():
    if request.method == "POST":
        username = request.cookies.get("username")
        password = request.cookies.get("password")
        reportId = request.form.get("reportId")

        deleteReportFunc(username, password, reportId)

        return "ok"
    return "false"


@app.route("/edit/<id>", methods=["GET", "POST"])
def editPage(id):

    if request.method == "GET":
        logged_in = isLoggedIn(request.cookies.get("username"), request.cookies.get("password"))

        entryim = entryBul(id)

        if logged_in:
            if entryim["author"] == request.cookies.get("username") or isAdmin(request.cookies.get("username"), request.cookies.get("password")):
                return render_template("edit.html", logged_in=logged_in, entry=entryim)

        return redirect("/entry/"+id)

    if request.method == "POST":
        message = request.form.get("message")
        entryId = request.form.get("entryId")

        username = request.cookies.get("username")
        password = request.cookies.get("password")

        print(username, password, entryId, message)
        if isLoggedIn(username, password):
            editEntry(username, password, id, message)

        return redirect("/entry/"+id)


if __name__ == "__main__":
    app.run(debug=True)
