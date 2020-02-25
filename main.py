#!/usr/bin/python3.6
from flask import Flask, render_template, request, url_for, redirect
import sqlite3
from flask_bootstrap import Bootstrap
import paramiko
from time import gmtime, strftime
import random
import string

app=Flask(__name__, static_url_path= ('/static'))
Bootstrap(app)


@app.route('/')
def homepage():
        return render_template('homepage.html')

@app.route('/', methods = ['POST', 'GET'])
def genpwd():
        if request.method == 'POST':
                pwdlen = int(request.form['Password Length'])
                password_characters = string.ascii_letters + string.digits + string.punctuation
                passwords = ''.join(random.choice(password_characters) for i in range(pwdlen))
        return render_template('homepage.html', passwords = passwords)
@app.route('/genesys')
def report_genesys():
        con = sqlite3.connect("/opt/web_rp/database/record_rp.db")
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("select * from report_genesys")
        rows_genesys = cur.fetchall()
        return render_template('report-genesys.html', rows_genesys = rows_genesys)

@app.route('/pbx')
def report_pbx():
        con = sqlite3.connect("/opt/web_rp/database/record_rp.db")
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("select * from report_pbx")
        rows_pbx = cur.fetchall()
        return render_template('report-pbx.html', rows_pbx = rows_pbx)

if __name__ == '__main__':
   app.run(debug = True, host ='192.168.1.75', port = 8000)

