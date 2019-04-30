from flask import Flask, render_template, request, redirect, url_for, Response
import BhamCalConverter
import time
#from flask_recaptcha import ReCaptcha

#site_key = BhamCalConverter.getCAPTCHASiteKey()
#secret_key = BhamCalConverter.getCAPTCHASecretKey()

app = Flask(__name__)
app.config["DEBUG"] = True

#app.config.update(dict(
#    RECAPTCHA_ENABLED = True,
#    RECAPTCHA_SITE_KEY = site_key,
#    RECAPTCHA_SECRET_KEY = secret_key,
#))

#recaptcha = ReCaptcha()
#recaptcha.init_app(app)

BhamCalConverter.resetInUse()

@app.route("/", methods=["GET", "POST"])
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
        return render_template("timetable_page.html", error=False, message = "", stats = stats, warn = warn, warning = warning, info = info, infoMessage = infoMessage)
    email = request.form["email"]
    username = request.form["username"]
    password = request.form["password"]
    customTitle = request.form["customTitle"]
    try:
        shortenTitle = request.form["shortenTitle"]
        print("shortenTitle: " + shortenTitle)
        if shortenTitle == "on":
            shortenTitle = True
        else:
            shortenTitle = False
    except:
        shortenTitle = False

    #message = BhamCalConverter.run(email, username, password)
    message, mins = BhamCalConverter.runFromFlaskWithDB(email, username, password, shortenTitle, customTitle)
    if message == "done":
        stats = BhamCalConverter.getStats()
        return render_template("timetable_page.html", done=True, mins = mins, stats = stats)


    stats = BhamCalConverter.getStats()
    return render_template("timetable_page.html", error=True, message = message, stats = stats)

@app.route("/timetable/")
def timetable():
    return redirect(url_for('main'))

@app.route("/test/email/")
def testEmail():
    return render_template("email_template.html")

@app.route("/donate")
def donate():
    return render_template("donate_page.html")

@app.route("/timetable/donate")
def donateForward():
    return redirect(url_for('donate'))

@app.route("/test/email_inline/")
def testEmailInline():
    return render_template("email_inline.html")

@app.route("/stats")
def stats():
    stats = BhamCalConverter.getStats()
    return render_template("stats_page.html", stats = stats)

@app.route("/test/stats/")
def oldStats():
    return redirect(url_for('stats'))

@app.route("/stats/")
def oldStatsTwo():
    return redirect(url_for('stats'))

@app.route("/test/forms", methods=["GET", "POST","POSTTWO"])
def forms():
    if request.method == "GET":
        return render_template("test_forms.html", test = True)

    elif request.method == "POST":
        return "1"
    else:
        return "2"

@app.route("/test/redirect")
def testRedirect():
    return render_template("redirect_home.html")

@app.route("/timetable/credits/")
def credits():
    return render_template("credits_page.html")

@app.route("/share")
def share():
    return render_template("share_page.html")

@app.route("/timetable/share/")
def oldSshare():
    return redirect(url_for('share'))

@app.route("/share/")
def oldSshare2():
    return redirect(url_for('share'))

@app.route('/test/start')
def start():
	return render_template('test_index.html')

@app.route('/test/extends')
def extendsTest():
	return render_template('test_timetable_page.html', stats = BhamCalConverter.getStats())

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
