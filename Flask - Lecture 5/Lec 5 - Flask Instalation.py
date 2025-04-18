from flask import Flask

app=Flask(__name__)

mydata="HOME PAGE -----------!!!!!!_______"
contact="Contact us page !!!!!!!!"
#@app.get("/")    #OR
@app.route("/")
def get_data():
	return mydata
#@app.get("/contact")  #OR
@app.route("/contacts")
def get_contact():
	return contact

if __name__ == "__main__":
	app.run(debug=True,host="0.0.0.0",port=9000)   # By this host="0.0.0.0" , IPs in the same network can also access this.
