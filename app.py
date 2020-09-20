from flask import Flask, render_template,redirect, url_for, request, jsonify, session
#from flask_mysqldb import MySQL
import pymysql
import requests
import os
import datetime

conn = pymysql.connect(host='172.17.0.3',port=int(3306), user='root', passwd='Xoco_137946', db='top_main')

app = Flask(__name__, template_folder="templates", static_folder="static")

@app.route("/", methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        return 'Hello'
    else:
        return render_template("index.html", title="Wellcome")

@app.route("/publications", methods=['GET', 'POST'])
def pubs():
    if request.method == 'POST':
        return 'Hello'
    else:
        return render_template("table.html", title="Publications", results='results')

@app.route("/journalists", methods=['GET', 'POST'])
def journal():
    if request.method == 'POST':
        return 'Hello'
    else:
        return render_template("table.html", title="Journalists", results='results')

@app.route("/articles", methods=['GET', 'POST'])
def arts():
    if request.method == 'POST':
        return 'Hello'
    else:
        return render_template("table.html", title="Articles", results='results')

app.run(host='0.0.0.0', port=80)