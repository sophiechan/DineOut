from sqlalchemy import *
from sqlalchemy.pool import NullPool
from flask import Flask, request, render_template, g, redirect, Response, Blueprint

restaurant_bp = Blueprint('restaurants', __name__)

@restaurant_bp.route('/')
def index():
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

	return render_template("restaurants.html", **context)