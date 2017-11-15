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

@manager_bp.route('/<restid>/<dname>', methods=['DELETE'])
@login_required
def listRemoveRestaurant(restid, dname):
    if request.method == 'DELETE':
        try:
            cursor = g.conn.execute('''
                DELETE FROM Have_Dishes WHERE dname=%s AND restid=%s
            ''',(dname, restid))
            cursor.close()
            return "delete successfully!"
        except:
            return "delete not successfully!"

@manager_bp.route('/updateRest', methods = ['POST'])
@login_required
def updateRest():
    restid = request.form['restid']
    name = request.form['name']
    street_name = request.form['street_name']
    city = request.form['city']
    state = request.form['state']
    postal_code = request.form['postal_code']
    try:
        cursor = g.conn.execute('''
                UPDATE Restaurants SET name=%s,
                street_name=%s, city=%s, state=%s, postal_code=%s WHERE restid=%s
        ''',(name, street_name, city, state, postal_code, restid))
        cursor.close()
        flash('Update successfully!')
        return redirect('/restaurants/' + restid)
    except:
        flash('Update not successfully!')
        return redirect('/restaurants/' + restid)
