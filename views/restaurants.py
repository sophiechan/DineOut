from sqlalchemy import *
from sqlalchemy.pool import NullPool
from flask import Flask, request, render_template, g, redirect, Response, Blueprint
from flask_login import login_user, login_required, current_user

restaurant_bp = Blueprint('restaurants', __name__)

@restaurant_bp.route('/')
@login_required
def all_restaurants():
	if current_user.auth:
		_, mid = current_user.id.split(" ")
		cursor = g.conn.execute('''
			SELECT R.* FROM Restaurants AS R, Manage AS M WHERE R.restid=M.restid AND M.mid=%s ORDER BY R.restid
		''',(mid))
	else:
		cursor = g.conn.execute("SELECT * FROM Restaurants ORDER BY restid")
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
@login_required
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
	query = "SELECT * FROM Write_Review_About WHERE restid='" + str(restid) + "' ORDER BY dt DESC"
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

	print current_user.auth
	if current_user.auth:
		context = dict(rest_info = rest_info, dishes = dishes, reviews = reviews, rest_id = restid)
	else:
		_, uid = current_user.id.split(" ")
		cursor = g.conn.execute('''
			SELECT P.lname FROM PersonalLists_Save AS P
			WHERE
				P.did = %s
				AND P.lname NOT IN (SELECT lname FROM Contain WHERE did=%s AND restid=%s)
		''',(uid, uid, restid))
		lists = []
		for result in cursor:
		    lists.append(result[0])
		print lists
		cursor.close()
		context = dict(rest_info = rest_info, dishes = dishes, reviews = reviews, lists = lists, rest_id = restid)

	# render_template looks in the templates/ folder for files.
	# for example, the below file reads template/index.html

	return render_template("restaurant.html", **context)
