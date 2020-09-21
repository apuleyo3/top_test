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
    pub_id = results['id']
    pub_name = results['Name']
    pub_web = results['Web']
    pub_visitors = results['Visitors']
    pub_add = results['Address']
    pub_add2 = results['Address 2']
    pub_city = results['City']
    pub_state = results['State']
    pub_zip = results['Zip code']
    pub_country = results['Country']
    pub_market = results['Market']
    pub_notes = results['Notes']

    if request.method == 'POST':
        name = request.form['name']
        website = request.form['website'] or "None"
        visitors = request.form['visitor'] or 0
        address1 = request.form['address1'] or "None"
        address2 = request.form['address2'] or "None"
        city = request.form['city'] or "None"
        country = request.form['country'] or "None"
        state = request.form['state'] or "None"
        zipcode = request.form['zip-code'] or "None"
        market = request.form['market'] or "None"
        notes = request.form['notes'] or "None"
        pb = "INSERT INTO publication (`name`, `website`, `unique_visitors_per_month`, `address_1`, `address_2`, `city`, `state`,  `country`, `zip_code`, `media_market`, `notes`) VALUES (" 
        query = pb + "'" + str(name) + "','" + str(website) + "'," + str(visitors) + ",'" + str(address1) + "','" + str(address2) + "','" + str(city) + "','" + str(state) + "','" + str(country) + "'," + str(zipcode) + ",'" + str(market) + "','" + str(notes) + "')"
        cur = mysql.connection.cursor()
        cur.execute(query)
        #data = cur.fetchall()
        mysql.connection.commit()
        cur.close()
        return redirect('/publications')
    else:
        return render_template("table.html", title="Publications", action="publications", \
             table=zip(pub_id, pub_name, pub_web, pub_visitors, pub_add, pub_add2, pub_city, pub_state, pub_zip, pub_country, pub_market, pub_notes))

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
        #data = cur.fetchall()
        mysql.connection.commit()
        cur.close()
        return redirect("/journalists")
    else:

        ops = pd.read_sql_query("""SELECT id, name FROM publication""", conn)
        ids = ops['id']
        nms = ops['name']
        return render_template("table.html", title="Journalists",  action="journalists", iter=zip(ids, nms), \
             table=zip(results['id'], results['first_name'], results['last_name'], results['email'], results['phone_number'], results['language_spoken'], results['title'], results['linkedin'], results['twitter'], results['notes'], results['publication_id']))

@app.route("/articles", methods=['GET', 'POST'])
def arts():
    conn = pymysql.connect(host='172.17.0.3',port=int(3306), user='root', passwd='Xoco_137946', db='top_main')
    results = pd.read_sql_query("""SELECT * FROM article""", conn)

    if request.method == 'POST':
        name = "'" + request.form['name'] + "'" or "None"
        title = "'" + request.form['title'] + "'" or "None"
        subject = "'" + request.form['subject'] + "'" or "None"
        publish = request.form['publish'] or "None"
        jrn = request.form['journalist'] or 0

        qr = "SELECT `publication_id` FROM `journalist` WHERE `id` = " + request.form['journalist']
        pb = pd.read_sql_query(qr, conn)
        pb = list(pb.values)
        npb = str(pb[0][0])

        publish = "'" + publish.replace('/', '-') +  " 00:00:00" + "'"

        art = "INSERT INTO article (`name`, `title`, `subject`, `publish_time`, `publication_id`, `journalist_id`) VALUES ("
        query = art + name + "," + title + "," + subject + "," + publish + "," + npb + "," + str(jrn) + ")"
        cur = mysql.connection.cursor()
        cur.execute(query)
        #data = cur.fetchall()
        mysql.connection.commit()
        cur.close()

        return redirect("/articles")
    else:
        ops = pd.read_sql_query("""SELECT id, first_name, last_name FROM journalist""", conn)
        ids = ops['id']
        nms = ops['first_name']
        lms = ops['last_name']
        
        return render_template("table.html", title="Articles", action="articles", iter=zip(ids,nms,lms), \
             table=zip(results['id'], results['name'], results['title'], results['subject'], results['publish_time'], results['publication_id'], results['journalist_id']))

"""EDIT"""


@app.route("/publication/edit", methods=['GET', 'POST'])
def pub_edit():
    if request.method == 'POST':
        id = request.args['id']
    if 'id' in request.args:
        conn = pymysql.connect(host='172.17.0.3',port=int(3306), user='root', passwd='Xoco_137946', db='top_main')
        query = "SELECT * FROM publication WHERE `id` =" + str(request.args['id'])
        edt = pd.read_sql_query(query, conn)
        edt.columns = ['id', 'Name', 'Web', 'Visitors', 'Address', 'Address 2', 'City', 'State', 'Zip code', 'Country', 'Market', 'Notes']
        return render_template('parts/pub_edit.html', action="publications", val=edt.values)
    else:
        return redirect('/publications')

@app.route("/journalist/edit", methods=['GET', 'POST'])
def jrn_edit():

    if 'id' in request.args:
        conn = pymysql.connect(host='172.17.0.3',port=int(3306), user='root', passwd='Xoco_137946', db='top_main')
        query = "SELECT * FROM journalist WHERE `id` =" + str(request.args['id'])
        edt = pd.read_sql_query(query, conn)

        ops = pd.read_sql_query("""SELECT id, name FROM publication""", conn)
        ids = ops['id']
        nms = ops['name']

        return render_template('parts/jrn_edit.html', val=edt.values, action="journalists", iter=zip(ids, nms))
    else:
        return redirect('/journalists')

@app.route("/article/edit", methods=['GET', 'POST'])
def art_edit():
    if 'id' in request.args:
        conn = pymysql.connect(host='172.17.0.3',port=int(3306), user='root', passwd='Xoco_137946', db='top_main')
        query = "SELECT * FROM article WHERE `id` =" + str(request.args['id'])
        edt = pd.read_sql_query(query, conn)

        ops = pd.read_sql_query("""SELECT id, first_name, last_name FROM journalist""", conn)
        ids = ops['id']
        nms = ops['first_name']
        lms = ops['last_name']

        return render_template('parts/art_edit.html', val=edt.values, action="articles", iter=zip(ids, nms, lms))
    else:
        return redirect('/journalists')

"""DELETE"""

@app.route("/article/delete", methods=['GET'])
def del_art():
    if 'id' in request.args:
        query = "DELETE FROM article WHERE `id` =" + str(request.args['id'])
        cur = mysql.connection.cursor()
        cur.execute(query)
        mysql.connection.commit()
        cur.close()
        return redirect('/articles')

@app.route("/journalist/delete", methods=['GET'])
def del_jrn():
    if 'id' in request.args:
        query = "DELETE FROM journalist WHERE `id` =" + str(request.args['id'])
        cur = mysql.connection.cursor()
        cur.execute(query)
        mysql.connection.commit()
        cur.close()
        return redirect('/journalists')

@app.route("/publication/delete", methods=['GET'])
def del_pub():
    if 'id' in request.args:
        query = "DELETE FROM publication WHERE `id` =" + str(request.args['id'])
        cur = mysql.connection.cursor()
        cur.execute(query)
        mysql.connection.commit()
        cur.close()
        return redirect('/publications')

app.run(host='0.0.0.0', port=80)