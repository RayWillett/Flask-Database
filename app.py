from flask import Flask, render_template, request, g, make_response
import sqlite3
from time import time 

"""CONFIGURATION"""

app = Flask(__name__)
DATABASE = './database/test.sql'

@app.errorhandler(404)
def page_not_found(error):
	return render_template('page_not_found.html'), 404

@app.teardown_appcontext
def close_connection(exception):
	db = getattr(g, '_database', None)
	if db is not None:
		db.close()

"""ROUTES"""

@app.route('/')
def show_login():
	if request.cookies.get('username') is None:
		return render_template('login.html')
	else:
		return "logged in previously"

@app.route('/login/', methods=['POST'])
def handle_login():
	user_id = request.form.to_dict()['userid']
	employee = get_employee(user_id)
	response = make_response(employee)
	response.set_cookie('username', employee, expires=(int(time())+10));
	return response

@app.route('/feed/')
def show_feed_schedule():
	user = request.cookies.get('username')
	return render_template('feeding_schedule.html')

@app.route('/schedule/<id>')
@app.route('/schedule/')
def show_work_schedule(id=None):
	user = request.cookies.get('username')
	return render_template('work_schedule.html', schedules=construct_todays_schedule(id))

@app.route('/pens/')
def show_pens():
	return render_template('pens.html', pens=get_pens_data())

@app.route('/pets/')
def show_pets():
	return render_template('pens.html', pens=get_all_pets())

@app.route('/employees/<id>')
@app.route('/employees/')
def log_employee_in(id=None):
	if id is None:
		return 'error'
	if int(id) < 1:
		return 'error'
	return get_employee(id)

"""DATABASE INTERACTION"""

def get_employee(id):
	cur = get_db().cursor()
	cur.execute("SELECT * FROM EMPLOYEE WHERE enumb = {:s}".format(id))
	return str(cur.fetchone())

def get_pens_data():
	cur = get_db().cursor()
	cur.execute("SELECT * FROM PEN")
	return cur.fetchall()

def construct_todays_schedule(id=None):
	cur = get_db().cursor()
	test = cur.execute("SELECT * FROM EMPLOYEE JOIN SHIFT ON worker = enumb WHERE day = 0")
	return test.fetchall()

def get_all_pets(id=None):
	cur = get_db().cursor()
	cur.execute("SELECT * FROM PET")
	return cur.fetchall()

# def get_todays_schedule(id=None):
# 	cur = get_db().cursor()
# 	if id is None:
# 		cur.execute("SELECT * FROM SHIFT WHERE day = {:d}".format(get_date()))
# 	else:
# 		cur.execute("SELECT * FROM SHIFT WHERE worker = {:d}".format(int(id)))
# 	return cur.fetchall()

def get_db():
	db = getattr(g, '_database', None)
	if db is None:
		db = g._database = sqlite3.connect(DATABASE)
	return db

def get_date():
	return 0 #stubbed

"""RUN"""

if __name__ == '__main__':
	app.run(debug=True)