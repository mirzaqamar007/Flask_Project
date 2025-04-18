from flask import Flask,render_template,request,url_for
#from flaskext.mysql import MySQL
from flask_mysqldb import MySQL
from datetime import date
from time import time

app=Flask(__name__)
app.config['MYSQL_HOST']='put sql server IP or if using EC2 then put public IP'
app.config['MYSQL_USER']='username'
app.config['MYSQL_PASSWORD']=''
app.config['MYSQL_DB']='alnafi'
mysql=MySQL(app)

mydata="HOME PAGE -----------!!!!!!_______"
@app.route("/")
def index():
	return render_template("index.html")
@app.route("/Trainers")
def Trainers():
	return render_template("trainer_form.html", message="Data has been stored!")



@app.route("/Trainers_create", methods=['POST','GET'])
def Trainers_create():
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
		return render_template('trainer_form.html')
@app.route("/Trainers_display", methods=['POST','GET'])
def Trainers_display():
	cursor = mysql.connection.cursor()
	sql="select * from Trainers_Details"
	#sql = "select * from Trainers_Details where course='Devops'"
	cursor.execute(sql)
	row = cursor.fetchall()
	return render_template('trainer_report.html',output_data=row)
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
			return render_template('trainer_report.html', output_data=row)

@app.route("/jira")
def Jira():
	return render_template("Jira_Page.html", message="Data has been stored!")

if __name__ == "__main__":
	app.run(debug=True, host="0.0.0.0")