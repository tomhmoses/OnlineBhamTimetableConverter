from flask import Flask, render_template, request, redirect, url_for
import BhamCalConverter

app = Flask(__name__)
app.config["DEBUG"] = True

BhamCalConverter.resetInUse()

@app.route("/timetable/", methods=["GET", "POST"])
def main():
    if request.method == "GET":
        BhamCalConverter.trackVisit()
        stats = BhamCalConverter.getStats()
        warning = BhamCalConverter.getWarningMessage()
        warn = False
        if warning != "":
            warn = True
        return render_template("main_page.html", error=False, message = "", stats = stats, warn = warn, warning = warning)


    email = request.form["email"]
    username = request.form["username"]
    password = request.form["password"]

    #message = BhamCalConverter.run(email, username, password)
    message, mins = BhamCalConverter.runFromFlaskWithDB(email, username, password)
    if message == "done":
        stats = BhamCalConverter.getStats()
        return render_template("main_page.html", done=True, mins = mins, stats = stats)

    stats = BhamCalConverter.getStats()
    return render_template("main_page.html", error=True, message = message, stats = stats)

@app.route("/")
def timetable():
    return redirect(url_for('main'))

@app.route("/done/")
def done():
    return render_template("done_page.html")

@app.route("/test/email/")
def testEmail():
    return render_template("test_email.html")

@app.route("/test/stats/")
def stats():
    stats = BhamCalConverter.getStats()
    return render_template("stats_page.html", visits = stats["visits"], users = stats["users"])

@app.route("/share/")
def share():
    return render_template("share_page.html")

@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404
