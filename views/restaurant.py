from sqlalchemy import *
from sqlalchemy.pool import NullPool
from flask import Flask, request, render_template, g, redirect, Response, Blueprint

restaurant_bp = Blueprint('restaurants', __name__)

@restaurant_bp.route('/')
def index():
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

@restaurant_bp.route('/<int:restid>')
def single_restaurant(restid):

	# get single restaurant info
	query = "SELECT * FROM Restaurants WHERE restid='" + str(restid) + "'"
	cursor = g.conn.execute(query)
	paras = ["restid", "name", "street_name", "city", "state", "postal_code", "stars"]
	for result in cursor:
	    rest_info = {paras[i]:result[i] for i in range(0, len(paras))}
	cursor.close()

	# get all the reviews
	"""
		dt date,
    	comments text,
    	star int,
    	did int,
    	restid int,
	"""
	query = "SELECT * FROM Write_Review_About WHERE restid='" + str(restid) + "' ORDER BY dt"
	cursor = g.conn.execute(query)
	paras = ["dt", "comments", "star", "did", "restid"]
	reviews = []
	for result in cursor:
	    reviews.append({
	        paras[i]:result[i] for i in range(0, len(paras))
	    })
	cursor.close()

	# get all dishes
	query = "SELECT dname FROM Have_Dishes WHERE restid='" + str(restid) + "'"
	cursor = g.conn.execute(query)
	dishes = []
	for result in cursor:
	    dishes.append(result[0])
	cursor.close()

	context = dict(rest_info = rest_info, dishes = dishes, reviews = reviews)

	# render_template looks in the templates/ folder for files.
	# for example, the below file reads template/index.html

	return render_template("restaurant.html", **context)