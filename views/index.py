from sqlalchemy import *
from sqlalchemy.pool import NullPool
from flask import Flask, request, render_template, g, redirect, Response, Blueprint

index_bp = Blueprint('index', __name__)

@index_bp.route('/')
def index():
	"""
	request is a special object that Flask provides to access web request information:

	request.method:   "GET" or "POST"
	request.form:     if the browser submitted a form, this contains the data in the form
	request.args:     dictionary of URL arguments, e.g., {a:1, b:2} for http://localhost?a=1&b=2

	See its API: http://flask.pocoo.org/docs/0.10/api/#incoming-request-data
	"""

	"""
	CREATE TABLE Restaurants(
		restid SERIAL,
		name text,
		street_name text,
		city text,
		state text,
		postal_code int,
		stars real,
		PRIMARY KEY (restid)
	);
	"""

	# DEBUG: this is debugging code to see what request looks like
	print request.args

	cursor = g.conn.execute("SELECT * FROM Restaurants")
	paras = ["restid", "name", "street_name", "city", "state", "postal_code", "stars"]
	data = []
	for result in cursor:
		data.append({
			paras[i]:result[i] for i in range(0, len(paras))
		})  # can also be accessed using result[0]
	cursor.close()
	
	context = dict(data = data)

	# render_template looks in the templates/ folder for files.
	# for example, the below file reads template/index.html

	return render_template("index.html", **context)
