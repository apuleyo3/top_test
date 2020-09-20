from flask import Flask, render_template,redirect, url_for, request, jsonify, session
from flask_mysqldb import MySQL
import pandas as pd
import pymysql
import requests
import os
import datetime


app = Flask(__name__, template_folder="templates", static_folder="static")

mysql = MySQL(app)
app.config['MYSQL_HOST'] = '172.17.0.3'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Xoco_137946'
app.config['MYSQL_DB'] = 'top_main'

@app.route("/", methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        return 'Hello'
    else:
        return render_template("index.html", title="Wellcome")

@app.route("/publications", methods=['GET', 'POST'])
def pubs():
    conn = pymysql.connect(host='172.17.0.3',port=int(3306), user='root', passwd='Xoco_137946', db='top_main')
    results = pd.read_sql_query("""SELECT * FROM publication""", conn)
    results.columns = ['id', 'Name', 'Web', 'Visitors', 'Address', 'Address 2', 'City', 'State', 'Zip code', 'Country', 'Market', 'Notes']
    if request.method == 'POST':
        name = request.form['name']
        website = request.form['website']
        visitors = 34
        address1 = request.form['address1']
        address2 = request.form['address2']
        city = request.form['city']
        country = request.form['country']
        state = request.form['state']
        zipcode = request.form['zip-code']
        market = request.form['market']
        notes = request.form['notes']
        pb = "INSERT INTO publication (`name`, `website`, `unique_visitors_per_month`, `address_1`, `address_2`, `city`, `state`,  `country`, `zip_code`, `media_market`, `notes`) VALUES (" 
        query = pb + "'" + str(name) + "','" + str(website) + "'," + str(visitors) + ",'" + str(address1) + "','" + str(address2) + "','" + str(city) + "','" + str(state) + "','" + str(country) + "'," + str(zipcode) + ",'" + str(market) + "','" + str(notes) + "')"
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()
        mysql.connection.commit()
        cur.close()
        return render_template("table.html", title="Publications", results=results.to_html(classes="table"), action="publications", message='Success!')
    else:
        return render_template("table.html", title="Publications", results=results.to_html(classes="table"), action="publications")

@app.route("/journalists", methods=['GET', 'POST'])
def journal():
    conn = pymysql.connect(host='172.17.0.3',port=int(3306), user='root', passwd='Xoco_137946', db='top_main')
    results = pd.read_sql_query("""SELECT * FROM journalist""", conn)
    if request.method == 'POST':
        fname = "'" + request.form['fname'] + "'" or "None"
        lname = "'" + request.form['lname'] + "'" or "None"
        email = "'" + request.form['email'] + "'" or "None"
        phone = request.form['phone'] or 0
        lang = "'" + request.form['language'] + "'" or "None"
        title = "'" + request.form['title'] + "'" or " "
        linkedin = "'" + request.form['linkedin'] + "'" or "None"
        twitter = "'" + request.form['twitter'] + "'" or "None"
        notes = "'" + request.form['notes'] + "'" or "None"
        pub = "'" + request.form['publication'] + "'"
        jn = "INSERT INTO journalist (`first_name`, `last_name`, `email`, `phone_number`, `language_spoken`, `title`, `linkedin`, `twitter`, `notes`, `publication_id`) VALUES ("
        query = jn + fname + "," + lname + "," + email + "," + str(phone) + "," + lang + "," + title + "," + linkedin + "," + twitter + "," + notes + "," + pub + ")"
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()
        mysql.connection.commit()
        cur.close()
        return render_template("table.html", title="Publications", results=results.to_html(classes="table"), action="publications", message='Success!')
    else:
        ops = pd.read_sql_query("""SELECT id, name FROM publication""", conn)
        ids = ops['id']
        nms = ops['name']
        return render_template("table.html", title="Journalists", results=results.to_html(classes="table"), action="journalists", iter=zip(ids, nms))

@app.route("/articles", methods=['GET', 'POST'])
def arts():
    conn = pymysql.connect(host='172.17.0.3',port=int(3306), user='root', passwd='Xoco_137946', db='top_main')
    results = pd.read_sql_query("""SELECT * FROM article""", conn)
    
    if request.method == 'POST':
        return 'Hello'
    else:
        ops = pd.read_sql_query("""SELECT id, name FROM journalist""", conn)
        ids = ops['id']
        nms = ops['name']
        
        return render_template("table.html", title="Articles", results=results.to_html(classes="table"), action="articles", iter=zip(ids,nms))

app.run(host='0.0.0.0', port=80)