from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort,send_file
import os
import tv
import update_database

app = Flask(__name__)
 


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/", methods=['POST'])
def search():
    user=request.form['user']
    email=request.form['email']
    series=request.form['series']
    a=tv.main(user,email,series)
    print(a)
    return render_template("index.html",details=a)

@app.route("/update")
def update():
	update_database.run_update()
	return render_template("index.html")


if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(app.run(debug=True, port=os.getenv("PORT")))