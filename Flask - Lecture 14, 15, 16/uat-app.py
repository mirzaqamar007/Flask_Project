import re

import MySQLdb.cursors
from Demos.win32ts_logoff_disconnected import username
from flask import Flask,render_template,request,url_for,session
#from flaskext.mysql import MySQL
from flask_mysqldb import MySQL
from datetime import date
from time import time
from jira import JIRA
from werkzeug.utils import redirect

app=Flask(__name__)
app.config['MYSQL_HOST']=''
app.config['MYSQL_USER']=''
app.config['MYSQL_PASSWORD']='2'
app.config['MYSQL_DB']='alnafi'
mysql=MySQL(app)
app.secret_key ='sjdkjfsdkfjdskf@33434&'

mydata="HOME PAGE -----------!!!!!!_______"
@app.route("/")
def index():
	if 'loggedin' in session:
		return render_template("index.html",username=session['username'])
	return render_template("login_page.html")
@app.route("/Trainers")
def Trainers():
	if 'loggedin' in session:
		return render_template("trainer_form.html",username=session['username'])
	return render_template("login_page.html", message="Data has been stored!")



@app.route("/Trainers_create", methods=['POST','GET'])
def Trainers_create():
	if 'loggedin' in session:
		if request.method=="POST":
			fname=request.form['fname']
			lname = request.form['lname']
			design = request.form['design']
			course = request.form['course']
			cdate = date.today()
			sql= "INSERT INTO Trainers_Details (fname,lname,design,course,datetime) VALUES (%s,%s,%s,%s,%s)"
			val= (fname,lname,design,course,cdate)

			cursor = mysql.connection.cursor()

			cursor.execute(sql,val)

			mysql.connection.commit()

			cursor.close()
			#return ("DATA has been stored !!!!")
			return render_template('trainer_form.html',username=session['username'])
	return render_template("login_page.html", message="Data has been stored!")
@app.route("/Trainers_display", methods=['POST','GET'])
def Trainers_display():
	if 'loggedin' in session:
		cursor = mysql.connection.cursor()
		sql="select * from Trainers_Details"
		#sql = "select * from Trainers_Details where course='Devops'"
		cursor.execute(sql)
		row = cursor.fetchall()
		return render_template('trainer_report.html',output_data=row,username=session['username'])
	return render_template("login_page.html", message="Data has been stored!")
@app.route("/Trainers_filter", methods=['POST','GET'])
def Trainers_filter():
	if request.method=="POST":
		course_search=request.form['course']
		cursor = mysql.connection.cursor()
		if course_search== 'All':
			sql = "select * from Trainers_Details"
			cursor.execute(sql)
			row = cursor.fetchall()
			return render_template('trainer_report.html', output_data=row)

		else:
			sql= "select * from Trainers_Details where course=" +course_search
			cursor.execute(sql)
			row = cursor.fetchall()
			return render_template('trainer_report.html', output_data=row,username=session['username'])

@app.route("/jira")
def Jira():
	if 'loggedin' in session:
		return render_template("Jira_Page.html", message="Data has been stored!")
	return render_template("login_page.html", message="Data has been stored!")
@app.route("/jira_create", methods=["GET", "POST"])
def jira_create():
    if request.method == "POST":
        project = request.form['project']
        issuetype = request.form['issuetype']
        reporter = request.form['reporter']
        priority = request.form['priority']
        summary = request.form['summary']
        desc = request.form['desc']

        server = "https://qamardevops.atlassian.net/"
        user = "mirza.qamar68@gmail.com"
        apitoken = ""

        jira = JIRA(server=server, basic_auth=(user, apitoken))

        issue_dict = {
            'project': {'key': project},
            'summary': summary,
            'description': desc,
            'issuetype': {'name': issuetype},
            'priority': {'name': priority},
            'reporter': {'id': reporter}  # optional: only include if necessary
        }

        issue = jira.create_issue(fields=issue_dict)
        print(issue)
        return render_template("Jira_Page.html")
@app.route("/login_page")
def login_page():
	return render_template("login_page.html", message="Data has been stored!")


@app.route("/", methods=["POST","GET"])
def login():
	msg= ''
	if request.method== 'POST':
		username= request.form['username']
		password = request.form['password']
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('select * from users where username = %s and password = %s',(username,password))
		account = cursor.fetchone()
		print(account)
		if account:
				session['loggedin'] = True
				session['id'] = account ['id']
				session['username'] = account ['username']
				return render_template("index.html",username=session['username'])
		else:
			msg = 'Incorrect Username/Password!!!!!'
	return render_template("login_page.html",msg=msg)

@app.route("/logout", methods=["POST","GET"])
def logout():
	session.pop('loggedin',None)
	session.pop('id',None)
	session.pop('username',None)
	return redirect(url_for('login_page'))

@app.route("/register", methods=["POST","GET"])
def register():
	return render_template("register.html",message="Data has been stored!")

@app.route("/create_account", methods=["POST","GET"])
def create_account():
	if request.method== 'POST':
		username= request.form['username']
		password = request.form['password']
		email = request.form['email']
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('select * from users where username = %s',(username,))
		account = cursor.fetchone()
		print(account)
		if account:    #for users already exist
			msg="User already exist"
			return render_template('register.html',msg=msg)
		elif not re.match(r'[^@]+@[^@]+\.[^@]',email):   #correct email format
			msg="Please enter the valid Email Address"
			return render_template('register.html', msg=msg)
		else:
			cursor.execute('INSERT INTO users values (NULL, %s, %s, %s)',(username,password,email))
			mysql.connection.commit()
			msg="Successfully Register"
			return render_template('register.html', msg=msg)
	elif request.method=='POST':
		msg = "Please enter the details !!!!"
	return render_template('login_page.html')


if __name__ == "__main__":
	app.run(debug=True, host="0.0.0.0")
