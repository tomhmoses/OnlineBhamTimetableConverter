from flask import Flask, render_template, request
import BhamCalConverter

app = Flask(__name__)
app.config["DEBUG"] = True

#comments = []

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("main_page.html", error=False, message = "")


    email = request.form["email"]
    username = request.form["username"]
    password = request.form["password"]

    #message = BhamCalConverter.run(email, username, password)
    message = BhamCalConverter.runFromFlask(email, username, password)
    if message == "done":
        return message

    return render_template("main_page.html", error=True, message = message)