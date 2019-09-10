from flask import Flask, render_template, request, redirect, url_for, Response, jsonify
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


@app.route("/", methods=["GET"])
def main():
    if request.method == "GET":
        BhamCalConverter.trackVisit()
        return render_template("new/index.html")
    else:
        time.sleep(5)
        return "posted"

@app.route('/process', methods=['POST'])
def process():
	email = request.form['email']
	username = request.form['username']
	password = request.form['password']

	message = BhamCalConverter.runFromFlask2019(email, username, password)

	if message == "done":
	    return jsonify({'message' : 'Success! Please wait for the processing to be done. This may take up to an hour. If it takes longer than this please contact me so I can fix the issue.'})

	return jsonify({'error' : message})

@app.route('/_add_numbers')
def add_numbers():
    a = request.args.get('a', 0, type=int)
    b = request.args.get('b', 0, type=int)
    return jsonify(result=a + b)

# redirects:

@app.route("/timetable/")
def timetable():
    return redirect(url_for('main'))

@app.route("/new/")
def new():
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
