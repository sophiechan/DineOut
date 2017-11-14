#!/usr/bin/env python2.7

"""
Columbia's COMS W4111.001 Introduction to Databases
Example Webserver

To run locally:

		python server.py

Go to http://localhost:8111 in your browser.

A debugger such as "pdb" may be helpful for debugging.
Read about it online.
"""

import os
from sqlalchemy import *
from sqlalchemy.pool import NullPool
from flask import Flask, request, render_template, g, redirect, Response, flash, url_for
from views.restaurants import restaurant_bp
from views.user import user_bp
from views.managers import manager_bp
from flask_login import (LoginManager, UserMixin, login_user, logout_user, current_user, login_required, fresh_login_required)

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)
login_manager = LoginManager(app)

app.register_blueprint(restaurant_bp, url_prefix='/restaurants')
app.register_blueprint(user_bp, url_prefix='/users')
app.register_blueprint(manager_bp, url_prefix='/managers')

#
# The following is a dummy URI that does not connect to a valid database. You will need to modify it to connect to your Part 2 database in order to use the data.
#
# XXX: The URI should be in the format of:
#
#     postgresql://USER:PASSWORD@104.196.18.7/w4111
#
# For example, if you had username biliris and password foobar, then the following line would be:
#
#     DATABASEURI = "postgresql://biliris:foobar@104.196.18.7/w4111"
#
DATABASEURI = "postgresql://xc2364:8103a@35.196.90.148/proj1part2"


#
# This line creates a database engine that knows how to connect to the URI above.
#
engine = create_engine(DATABASEURI)

#
# Example of running queries in your database
# Note that this will probably not work if you already have a table named 'test' in your database, containing meaningful data. This is only an example showing you how to run queries in your database using SQLAlchemy.
#
engine.execute("""CREATE TABLE IF NOT EXISTS test (
	id serial,
	name text
);""")
engine.execute("""INSERT INTO test(name) VALUES ('grace hopper'), ('alan turing'), ('ada lovelace');""")


@app.before_request
def before_request():
	"""
	This function is run at the beginning of every web request
	(every time you enter an address in the web browser).
	We use it to setup a database connection that can be used throughout the request.

	The variable g is globally accessible.
	"""
	try:
		g.conn = engine.connect()
	except:
		print "uh oh, problem connecting to database"
		import traceback; traceback.print_exc()
		g.conn = None

@app.teardown_request
def teardown_request(exception):
	"""
	At the end of the web request, this makes sure to close the database connection.
	If you don't, the database could run out of memory!
	"""
	try:
		g.conn.close()
	except Exception as e:
		pass


#
# @app.route is a decorator around index() that means:
#   run index() whenever the user tries to access the "/" path using a GET request
#
# If you wanted the user to go to, for example, localhost:8111/foobar/ with POST or GET then you could use:
#
#       @app.route("/foobar/", methods=["POST", "GET"])
#
# PROTIP: (the trailing / in the path is important)
#
# see for routing: http://flask.pocoo.org/docs/0.10/quickstart/#routing
# see for decorators: http://simeonfranklin.com/blog/2012/jul/1/python-decorators-in-12-steps/
#

# @app.route('/')
# def index():

# 	"""
# 	request is a special object that Flask provides to access web request information:

# 	request.method:   "GET" or "POST"
# 	request.form:     if the browser submitted a form, this contains the data in the form
# 	request.args:     dictionary of URL arguments, e.g., {a:1, b:2} for http://localhost?a=1&b=2

# 	See its API: http://flask.pocoo.org/docs/0.10/api/#incoming-request-data
# 	"""

# 	# DEBUG: this is debugging code to see what request looks like
# 	print request.args


# 	#
# 	# example of a database query
# 	#
# 	cursor = g.conn.execute("SELECT name FROM test")
# 	names = []
# 	for result in cursor:
# 		names.append(result['name'])  # can also be accessed using result[0]
# 	cursor.close()

# 	#
# 	# Flask uses Jinja templates, which is an extension to HTML where you can
# 	# pass data to a template and dynamically generate HTML based on the data
# 	# (you can think of it as simple PHP)
# 	# documentation: https://realpython.com/blog/python/primer-on-jinja-templating/
# 	#
# 	# You can see an example template in templates/index.html
# 	#
# 	# context are the variables that are passed to the template.
# 	# for example, "data" key in the context variable defined below will be
# 	# accessible as a variable in index.html:
# 	#
# 	#     # will print: [u'grace hopper', u'alan turing', u'ada lovelace']
# 	#     <div>{{data}}</div>
# 	#
# 	#     # creates a <div> tag for each element in data
# 	#     # will print:
# 	#     #
# 	#     #   <div>grace hopper</div>
# 	#     #   <div>alan turing</div>
# 	#     #   <div>ada lovelace</div>
# 	#     #
# 	#     {% for n in data %}
# 	#     <div>{{n}}</div>
# 	#     {% endfor %}
# 	#
# 	context = dict(data = names)


# 	#
# 	# render_template looks in the templates/ folder for files.
# 	# for example, the below file reads template/index.html
# 	#
# 	return render_template("index.html", **context)

#
# This is an example of a different path.  You can see it at:
#
#     localhost:8111/another
#
# Notice that the function name is another() rather than index()
# The functions for each app.route need to have different names
#
# @app.route('/another')
# def another():
# 	return render_template("another.html")


# # Example of adding new data to the database
# @app.route('/add', methods=['POST'])
# def add():
# 	name = request.form['name']
# 	g.conn.execute('INSERT INTO test VALUES (NULL, ?)', name)
# 	return redirect('/')


# @app.route('/login')
# def login():
# 		abort(401)
# 		this_is_never_executed()

login_manager.login_view = 'login'
login_manager.login_message = 'Unauthorized User'
login_manager.login_message_category = "info"

users = []

class User(UserMixin):
    auth = True
    username = ""

    def hasAuth(self):
        return 'Manager' if self.auth else 'Diner'

def query_user(id):
    for user in users:
        if user['id'] == id:
            return user

@login_manager.user_loader
def load_user(id):
	user_info = query_user(id)
	if user_info is not None:
		curr_user = User()
		curr_user.id = user_info['id']
		curr_user.auth = user_info['auth']
		curr_user.username = user_info['username']
		return curr_user
    # Must return None if username not found

# @login_manager.request_loader
#     username = request.args.get('token')
#     user = query_user(username)
#     if user is not None:
#         curr_user = User()
#         curr_user.id = username
#         return curr_user
#     # Must return None if username not found

@login_manager.unauthorized_handler
def unauthorized_handler():
    return 'Unauthorized'

@app.route('/')
def index():
	if current_user.is_authenticated:
		_, uid = current_user.id.split(" ")
		if not current_user.auth:
			query = "SELECT lname FROM PersonalLists_Save WHERE did='" + uid + "'"
			cursor = g.conn.execute(query)
			lists = [ele[0] for ele in cursor]
			cursor.close()
			return render_template('hello.html', lists=lists)
		else:
			return render_template('hello.html')
	else:
		return "<a href='/login'>Log In</h>"

@app.route('/home')
@fresh_login_required
def home():
    return 'Logged in as: %s' % current_user.get_id()

# consider the user name as unique
@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		username = request.form.get('username')

		if username:
			auth = True if request.form['auth'] == "true" else False
			dbName = "Managers" if auth else "Diners"
			password = request.form['password']

			query = "SELECT * FROM " + dbName + " WHERE name='" + username +"' AND password='" + password + "'"
			cursor = g.conn.execute(query)
			rows = cursor.fetchall()
			cursor.close()
			if len(rows):
				curr_user = User()

				user_id = "M " if auth else "D "
				user_id = user_id + str(rows[0][0])
				curr_user.auth = auth
				curr_user.id = user_id
				curr_user.username = username
				users.append(
					{"id":user_id, "auth":auth, "username":username}
				)
				cursor.close()
				next = request.args.get('next')
				login_user(curr_user, remember=True)
				return redirect(next or url_for('index'))
				 # can also be accessed using result[0]
			cursor.close()

        # if user is not None and request.form['password'] == user['password']:
        #     print request.form['auth']
        #     curr_user = User()
        #     curr_user.id = username

        #     login_user(curr_user, remember=True)

        #     next = request.args.get('next')
        #     return redirect(next or url_for('index'))

		flash('Wrong username or password!')
	return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return 'Logged out successfully!'

app.secret_key = '1234567'

if __name__ == "__main__":
	import click

	@click.command()
	@click.option('--debug', is_flag=True)
	@click.option('--threaded', is_flag=True)
	@click.argument('HOST', default='0.0.0.0')
	@click.argument('PORT', default=8111, type=int)
	def run(debug, threaded, host, port):
		"""
		This function handles command line parameters.
		Run the server using:

				python server.py

		Show the help text using:

				python server.py --help

		"""

		HOST, PORT = host, port
		print "running on %s:%d" % (HOST, PORT)
		app.run(host=HOST, port=PORT, debug=debug, threaded=threaded)
	run()
