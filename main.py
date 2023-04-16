from flask import Flask, render_template, request, redirect, url_for, session, abort, flash,Response
import random
import mysql.connector
import datetime
import asyncio
import json
import sqlite3
import os
import time
import ast
from connection import  DBO


app = Flask(__name__)
app.debug = True
app.secret_key = 'app@Telegram'

@app.route("/")
def pc():
	return redirect("/m")
@app.before_request
def before_request():
    #'''
    if not request.is_secure:
        url = request.url.replace('http://', 'https://', 1)
        code = 301
        return redirect(url, code=code)
    #'''
    #pass

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

def fetchApi(**argv):
	if len(argv) == 2:
		data = ({"success":False,})
		try:
			db = DB()
			cur = db.cursor(buffered=True)
			cur.execute("select * from users where email_id = %s and password = %s",(argv[0],argv[1],))
			exists = cur.fetchone()
			if exists:
				data = ({"success":True,"key":exists[0],})
		except:
			data = ({"success":False,})
			pass
		finally:
			return data

@app.route("/m/api/<q>",methods=['GET','POST'])
def api(q):
	photos = [1,2,3,4,5,6,7,8,9,10]
	services = [1,2,3]
	if q == "home":
		return render_template("mobile/home.html", **locals())
	elif q == "contact":
		return render_template("mobile/contact.html", **locals())
	elif q == "about" or q == "services":
		return render_template("mobile/services.html",**locals())
	elif q == "gallery":
		if session.get("user") != None:
			return render_template("mobile/login.html",**locals())
		else:
			return render_template("mobile/gallery.html",**locals())
	elif q == "login":
		if request.method == "POST" and "email" in request.form:
			email = request.form
			password = reques.form
			data = fetchApi(email,password)
		return render_template("mobile/login.html",**locals())
	elif q == "signup":
		return render_template("mobile/signup.html",**locals())
	elif q == "artists":
		return render_template("mobile/about.html")
	elif q == "settings":
		return render_template("mobile/settings.html")
	elif q == "edit":
		return render_template("mobile/user-settings.html")
	#return render_template("mobile/index.html")

@app.route("/m/")
def mobileHome():
	photos = [1,2,3,4,5,6,7,8,9,10]
	return render_template("mobile/index.html", **locals())

@app.route("/m/<page>")
def mobilePage(page):
	if page == "services":
		return render_template("mobile/services.html")
	if page == "contact":
		return render_template("mobile/contact.html")
	else:
		return redirect("/m/")

if __name__=="__main__":
	app.run("0.0.0.0")