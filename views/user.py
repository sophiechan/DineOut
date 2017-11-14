from sqlalchemy import *
from sqlalchemy.pool import NullPool
from flask import Flask, request, render_template, g, redirect, Response, Blueprint, url_for, flash
from flask_login import login_user, login_required, current_user

user_bp = Blueprint('users', __name__)

@user_bp.route('/<lname>', methods=['GET', 'POST', 'DELETE'])
def personList(lname):
    if request.method == 'GET':
        _, uid = current_user.id.split(" ")
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
        return render_template("perlist.html", data=data)

    if request.method == 'DELETE':
        pass


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
