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


@app.route("/download")
def report_download():
    pdf = FPDF()
    pdf.set_font("Arial", 'B',size=12)
    pdf.add_page()

    pdf.image("logo.jpg", x=10, y=15, w=50)
    pdf.cell(200,15, txt="Report", ln=1, align="C")
    date=datetime.datetime(2019, 6, 23, 7, 31, 46)
    b=[]
    print("HELLO")
    print(a)
    for key,value in a.items():
        b.append([key,value])

    flag=0
    pdf.set_font("Arial",size=12)
    col_width = pdf.w / 4.5
    row_height = pdf.font_size
    pdf.ln(row_height*10)
    for row in b:
        for item in row:
            if(isinstance(item,list)):
                for sd in item:
                    pdf.cell(col_width, row_height,
                        txt=sd, border=1)
                    flag+=1
                    if(flag<len(item)):
                        pdf.ln(row_height)
                        pdf.cell(col_width, row_height,
                            txt="", border=1)
            else:
                pdf.cell(col_width, row_height,
                            txt=item, border=1)
        pdf.ln(row_height)

    pdf.output('report.pdf')


    return send_file("report.pdf")


if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(app.run(debug=True, port=os.getenv("PORT")))