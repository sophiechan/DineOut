from sqlalchemy import *
from sqlalchemy.pool import NullPool
from flask import Flask, request, render_template, g, redirect, Response, Blueprint, url_for, flash
from flask_login import login_user, login_required, current_user

manager_bp = Blueprint('managers', __name__)

@manager_bp.route('/addDish', methods=['POST'])
@login_required
def addDish():
    restid = request.form['restid']
    if request.method == 'POST' and request.form['dname']:
        # _, mid = current_user.id.split(" ")
        query = "INSERT INTO Have_Dishes (restid, dname) VALUES ('"+ restid + "', '" + request.form['dname'] + "')"
        try:
            cursor = g.conn.execute(query)
            cursor.close()
        except:
            flash('Duplicate Name')
    else:
        flash('Empty Input Error')
    return redirect('/restaurants/' + restid)
