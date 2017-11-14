from sqlalchemy import *
from sqlalchemy.pool import NullPool
from flask import Flask, request, render_template, g, redirect, Response, Blueprint, url_for, flash
from flask_login import login_user, login_required, current_user

user_bp = Blueprint('users', __name__)

@user_bp.route('/<lname>', methods=['GET', 'POST', 'DELETE'])
def personList(lname):
    _, uid = current_user.id.split(" ")
    if request.method == 'GET':
        # query = "SELECT R.* FROM Restaurants AS R, Contain AS C WHERE C.did='" + uid + "', C.lname='" + lname + "' AND R.restid=C.restid"
        cursor = g.conn.execute('''
            SELECT R.* FROM Restaurants AS R, Contain AS C WHERE C.did=%s AND C.lname=%s AND R.restid=C.restid
        ''',(uid, lname))
        paras = ["restid", "name", "street_name", "city", "state", "postal_code", "stars"]
        data = []
        for result in cursor:
            data.append({
        		paras[i]:result[i] for i in range(0, len(paras))
        	})
        cursor.close()
        return render_template("perlist.html", data=data, lname=lname)

    if request.method == 'DELETE':
        try:
            cursor = g.conn.execute('''
                DELETE FROM PersonalLists_Save WHERE did=%s AND lname=%s
            ''',(uid, lname))
            cursor.close()
            return "delete successfully!"
        except:
            return "delete not successfully!"

@user_bp.route('/addList', methods=['POST'])
@login_required
def addList():
    if request.method == 'POST' and request.form['lname']:
        _, uid = current_user.id.split(" ")
        query = "INSERT INTO PersonalLists_Save (did, lname) VALUES ('"+ uid + "', '" + request.form['lname'] + "')"
        try:
            cursor = g.conn.execute(query)
            cursor.close()
        except:
            flash('Duplicate keys!!!')
    else:
        flash('Empty input error!!!')
    return redirect('/')

@user_bp.route('/<lname>/<restid>', methods=['DELETE'])
@login_required
def listRemoveRestaurant(lname, restid):
    if request.method == 'DELETE':
        _, uid = current_user.id.split(" ")
        try:
            cursor = g.conn.execute('''
                DELETE FROM Contain WHERE did=%s AND lname=%s AND restid=%s
            ''',(uid, lname, restid))
            cursor.close()
            return "delete successfully!"
        except:
            return "delete not successfully!"

@user_bp.route('/addReview', methods=['POST'])
@login_required
def addReview():
    if request.method == 'POST' and request.form['comment'] and request.form['star']:
        _, uid = current_user.id.split(" ")
        comments = request.form['comment']
        star = request.form['star']
        restid = request.form['restid']
        from datetime import date
        today = date.today()
        try:
            cursor = g.conn.execute('''
                INSERT INTO Write_Review_About (dt, comments, star, did, restid) VALUES (%s, %s, %s, %s, %s)
            ''',(today.isoformat(), comments, star, uid, restid))
            cursor.close()

            # recalculate the star of this restaurant
            cursor = g.conn.execute('''
                UPDATE Restaurants SET stars=(SELECT AVG(star) FROM Write_Review_About WHERE restid=%s) WHERE restid=%s
            ''',(restid, restid))
            cursor.close()
        except:
            flash('Duplicate keys!!!')
    else:
        flash('Empty input error!!!')
    return redirect('/restaurants/' + restid)
