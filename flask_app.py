from flask import Flask, render_template, request, redirect, url_for
import BhamCalConverter

app = Flask(__name__)
app.config["DEBUG"] = True

#comments = []

@app.route("/timetable/", methods=["GET", "POST"])
def main():
    if request.method == "GET":
        return render_template("main_page.html", error=False, message = "")


    email = request.form["email"]
    username = request.form["username"]
    password = request.form["password"]

    #message = BhamCalConverter.run(email, username, password)
    message = BhamCalConverter.runFromFlask(email, username, password)
    if message == "done":
        return redirect(url_for('done'))

    return render_template("main_page.html", error=True, message = message)

@app.route("/")
def timetable():
    return redirect(url_for('main'))

@app.route("/done/")
def done():
    return render_template("done_page.html")

@app.route("/test/email/")
def testEmail():
    return render_template("test_email.html")

@app.route("/share/")
def share():
    return render_template("share_page.html")
