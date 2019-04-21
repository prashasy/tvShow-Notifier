from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort,send_file
import os
import whois_lookup
from fpdf import FPDF
import datetime
 
app = Flask(__name__)
 

a={}
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/", methods=['POST'])
def search():
    global a
    user=request.form['user']
    email=request.form['email']
    series=request.form['series']
    a=tv.main(user,email,series)
    return render_template("index.html",details=a)




if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(app.run(debug=True, port=os.getenv("PORT")))