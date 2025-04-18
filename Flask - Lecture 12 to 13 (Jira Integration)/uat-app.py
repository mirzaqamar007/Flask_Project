from flask import Flask,render_template,request,url_for
#from flaskext.mysql import MySQL
from flask_mysqldb import MySQL
from datetime import date
from time import time
from jira import JIRA

app=Flask(__name__)
app.config['MYSQL_HOST']=''
app.config['MYSQL_USER']=''
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




if __name__ == "__main__":
	app.run(debug=True, host="0.0.0.0")
