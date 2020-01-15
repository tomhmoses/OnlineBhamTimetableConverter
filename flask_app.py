from flask import Flask, render_template, request, redirect, url_for, Response, jsonify
from twilio.twiml.messaging_response import MessagingResponse
import BhamCalConverter
import time
import requests
import pickle

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

@app.route("/sms2", methods=['GET', 'POST'])
def incoming_sms2():
    """Send a dynamic reply to an incoming text message"""
    # Get the message the user sent our Twilio number
    body = request.values.get('Body', None)

    # Start our TwiML response
    resp = MessagingResponse()

    # Determine the right reply for this message
    if body == 'hello':
        resp.message("Hi!")
    elif body == 'bye':
        resp.message("Goodbye")
    elif body == None:
        resp.message("Got none")
    elif "dog" in body and "cat" in body:
        resp.message("To be honest and boring, it depends on the sort of relationship you want with your pet. If you want a little buddy that adores you and wants to partake in your life all the time, get a dog. If you want a pet that's more like a roommate providing ambient companionship, seemingly living their own busy life along with being soft and cuddly some of the time, get a cat. And I think cats are hilarious, because they act as if they need to maintain an air of dignity and composure, but constantly fail to do so.")


    return str(resp)

@app.route("/sms", methods=['GET', 'POST'])
def incoming_sms():
    """Send a dynamic reply to an incoming text message"""
    # Get the message the user sent our Twilio number
    body = request.values.get('Body', None)

    # Start our TwiML response
    resp = MessagingResponse()
    resp.message("getting your answer...")

    # Determine the right reply for this message
    if body == None:
        resp.message("Got none!")
    elif body.lower == 'bye':
        resp.message("Goodbye")
    elif "fab or hackthemidlands" in body.lower():
        resp.message("Okay, we can figure this out...\n 1. Goto Hack the midlands, \n2. Go to fab\n 3.[removed as under 18's in audience] \n4. go back and re-write your entire hack!")
    elif "hackthemidlands" in body.lower():
        resp.message("Goodbye")
    else:
        params = {
            "q" : body,
            "format" : "json"
            }
        r = requests.get("https://api.duckduckgo.com/", params = params)
        data = r.json()
        t = data["AbstractText"]
        if t == "":
            t = "none found"
        resp.message(t)

    return str(resp)



@app.route("/pay", methods=["GET"])
def payMain():
    BhamCalConverter.trackVisit()
    return render_template("new/index-pay.html")

@app.route('/process', methods=['POST'])
def process():
	email = request.form['email']
	username = request.form['username']
	password = request.form['password']

	message, queueLength = BhamCalConverter.runFromFlask2019(email, username, password)

	if message == "done":
	    return jsonify({'message' : 'Success! Please wait for the processing to be done. This may take up to an hour. If it takes longer than this please contact me so I can fix the issue.','queueLength' : queueLength})

	return jsonify({'error' : message})

@app.route('/jump', methods=['PUT'])
def queueJump():
    username = request.form['username']
    person = request.form['person']
    password = request.form['password']
    how = request.form['how']
    message = BhamCalConverter.queueJump(username, person, password, how)
    return jsonify({'message' : message})

@app.route("/jumper", methods=["GET"])
def jumper():
    return render_template("new/jumper.html")

@app.route("/reviews")
def reviews():
    return render_template("new/reviews.html")


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

#@app.route('/test/progress')
#def progress():
#	def generate():
#		x = 0
#
#		while x <= 100:
#			yield "data:" + str(x) + "\n\n"
#			x = x + 10
#			time.sleep(2)
#
#	return Response(generate(), mimetype= 'text/event-stream')

@app.route("/ubmc/countdown")
def ubmc_countdown():
    return render_template("/ubmc/countdown.html", cd_dict = pickle.load( open( "templates/ubmc/cd_dict.p", "rb" ) ))

@app.route("/ubmc/set/", methods=["GET", "POST"])
def ubmc_set():
    if request.method == "GET":
        return render_template("/ubmc/set.html")

    if request.form["password"] == pickle.load( open( "templates/ubmc/password.p", "rb")):
        countdown_dict = {"datetime":UBMCDateFormater(request.form["datetime"]),"url":request.form["url"]}
        pickle.dump( countdown_dict, open( "templates/ubmc/cd_dict.p", "wb" ) )
        return "worked, set for: " + UBMCDateFormater(request.form["datetime"]) + "was: " + request.form["datetime"]
    else:
        return "fail"

    return "other option!"

def UBMCDateFormater(st):
    st = st.replace("-",",").replace("T",",").replace(":",",").split(",")
    st = [st[0],str(int(st[1])-1),st[2],st[3],st[4],"05"]
    st = ", ".join(st)
    return st

@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404
