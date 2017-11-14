from sqlalchemy import *
from sqlalchemy.pool import NullPool
from flask import Flask, request, render_template, g, redirect, Response, Blueprint, url_for, flash
from flask_login import login_user, login_required

user_bp = Blueprint('users', __name__)

@user_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        user = query_user(username)

        if user is not None and request.form['password'] == user['password']:
            curr_user = User()
            curr_user.id = username

            login_user(curr_user)

            next = request.args.get('next')
            return redirect(next or url_for('restaurants'))

        flash('Wrong username or password!')

    return render_template('login.html')

@user_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return 'Logged out successfully!'