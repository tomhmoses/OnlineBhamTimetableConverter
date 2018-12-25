from flask import Flask, render_template, request, redirect, url_for, Response
import BhamCalConverter
import time
from flask_recaptcha import ReCaptcha

site_key = BhamCalConverter.getCAPTCHASiteKey()
secret_key = BhamCalConverter.getCAPTCHASecretKey()

app = Flask(__name__)
app.config["DEBUG"] = True

app.config.update(dict(
    RECAPTCHA_ENABLED = True,
    RECAPTCHA_SITE_KEY = site_key,
    RECAPTCHA_SECRET_KEY = secret_key,
))

recaptcha = ReCaptcha()
recaptcha.init_app(app)

BhamCalConverter.resetInUse()

@app.route("/timetable/", methods=["GET", "POST"])
def main():
    if request.method == "GET":
        BhamCalConverter.trackVisit()
        stats = BhamCalConverter.getStats()
        warning = BhamCalConverter.getWarningMessage()
        infoMessage = BhamCalConverter.getInfoMessage()
        warn = False
        if warning != "":
            warn = True
        info = False
        if infoMessage != "":
            info = True
        return render_template("main_page.html", error=False, message = "", stats = stats, warn = warn, warning = warning, info = info, infoMessage = infoMessage)

    if recaptcha.verify():
        email = request.form["email"]
        username = request.form["username"]
        password = request.form["password"]

        #message = BhamCalConverter.run(email, username, password)
        message, mins = BhamCalConverter.runFromFlaskWithDB(email, username, password)
        if message == "done":
            stats = BhamCalConverter.getStats()
            return render_template("main_page.html", done=True, mins = mins, stats = stats)
    else:
        message = "Failed reCAPTCHA"

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
    return render_template("stats_page.html", stats = stats)

@app.route("/test/forms/", methods=["GET", "POST","POSTTWO"])
def forms():
    if request.method == "GET":
        return render_template("test_forms.html", test = True)

    elif request.method == "POST":
        return "1"
    else:
        return "2"

@app.route("/share/")
def share():
    return render_template("share_page.html")

@app.route('/test/start')
def start():
	return render_template('test_index.html')

@app.route('/test/progress')
def progress():
	def generate():
		x = 0

		while x <= 100:
			yield "data:" + str(x) + "\n\n"
			x = x + 10
			time.sleep(2)

	return Response(generate(), mimetype= 'text/event-stream')

@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404
