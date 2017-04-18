from flask import Flask, render_template, request, g, make_response, url_for, redirect, Response
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
def index():
	if request.cookies.get('username') is None:
		return render_template('login.html')
	else:
		user_id = request.cookies.get('username')
		employee = get_employee(user_id)
		response = make_response(render_template('index.html', user=employee))
		return response

@app.route('/login/', methods=['POST'])
def handle_login():
	user_id = request.form.to_dict()['userid']
	employee = get_employee(user_id)
	response = redirect('/', code=302)
	response.set_cookie('username', str(employee[0]), expires=(int(time())+10));
	return response

@app.route('/feed/')
def show_feed_schedule():
	user = request.cookies.get('username')
	return render_template('feeding_schedule.html', pens=get_pens_data())

@app.route('/feedPen/', methods=['POST'])
def update_pen_feed_status():
	pen_id = request.form.to_dict()['penid']
	update_pen_in_database(pen_id)
	response = redirect('/feed/', code=302)
	return response

@app.route('/schedule/<id>')
@app.route('/schedule/')
def show_work_schedule(id=None):
	user = request.cookies.get('username')
	return render_template('work_schedule.html', schedules=construct_todays_schedule(id))

@app.route('/pets/')
def show_pets():
	return render_template('pets.html', newpet=False, pets=get_all_pets())

@app.route('/newpet/', methods=["POST"])
def register_pet():
	form = request.form.to_dict()
	insert_pet_into_db(form)
	response = redirect('/pets/', code=302)
	return response

"""DATABASE INTERACTION"""

def update_pen_in_database(pen_id):
	db = get_db()
	curr = db.cursor()
	curr.execute("UPDATE PEN SET finished=1 WHERE id={:s}".format(pen_id))
	db.commit()
	return

def insert_pet_into_db(values):
	db = get_db()
	cur = db.cursor()
	owner_phone = values['contact']
	fname = values['fname']
	lname = values['lname']

	pet_name = values['pname']
	date_in = values['datein']
	date_out = values['dateout']

	pen = update_pen_capacity()

	if pen == -1:
		return
	cur.execute("SELECT * FROM CUSTOMER WHERE phone='{:s}'".format(owner_phone))

	if cur.fetchone() is None:
		cur.execute("INSERT INTO CUSTOMER VALUES ('{:s}','{:s}','{:s}')".format(fname, lname, owner_phone))
	cur.execute("INSERT INTO PET VALUES ('{:s}',{:s},{:s},'{:s}',{:d})".format(pet_name, date_in, date_out, owner_phone, pen))
	db.commit()
	return

def get_employee(id):
	cur = get_db().cursor()
	cur.execute("SELECT * FROM EMPLOYEE WHERE enumb = {:s}".format(id))
	return cur.fetchone()

def get_pens_data():
	cur = get_db().cursor()
	cur.execute("SELECT id, fill, capacity, fname, lname, finished FROM PEN JOIN EMPLOYEE ON enumb=worker")
	return cur.fetchall()

def construct_todays_schedule(id=None):
	cur = get_db().cursor()
	test = cur.execute("SELECT * FROM EMPLOYEE JOIN SHIFT ON worker = enumb WHERE day = 0")
	return test.fetchall()

def get_all_pets(id=None):
	cur = get_db().cursor()
	cur.execute("SELECT name, fname, lname, phone, pen, date_in, date_out FROM PET JOIN CUSTOMER ON phone=owner")
	return cur.fetchall()

def update_pen_capacity():
	curr = get_db().cursor()
	curr.execute("SELECT id FROM PEN WHERE fill < capacity")
	open_pen = int(curr.fetchone()[0])
	if open_pen is None:
		return -1
	curr.execute("UPDATE PEN SET fill = fill + 1")
	return open_pen

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