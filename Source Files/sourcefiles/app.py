from flask import Flask,render_template
from flask import jsonify
import MySQLdb
import json
import led

app = Flask(__name__)

#Retrieve from the Database the Past Temps in an HTML Table
@app.route("/temps")
def temps(): #Get the past temps from the database and render them into an HTML Table
 db = MySQLdb.connect("localhost","pi","secret","IT715Project" )
 cursor = db.cursor()
 query = "select id,date,time,time2,temp,humidity,soil from temps ORDER BY id DESC Limit 50" #SQL Script
 cursor.execute(query)
 data = cursor.fetchall() #Fetch the ata and put it into a data object
 db.close() #Close the Database
 return render_template('pastTemps.html', data=data)

#Retrieve from the Database the latest recordings and display on a HTML Page
@app.route("/")
def index():
 db = MySQLdb.connect("localhost","pi","secret","IT715Project" )
 cursor = db.cursor()
 query = "select id,date,time,time2,temp,humidity,soil from temps ORDER BY id DESC LIMIT 1" #Get latest data in the SQL Table
 cursor.execute(query)
 data2 = cursor.fetchall() #Fetch the ata and put it into a data object
 db.close() #Close the Database
 return render_template('index.html', data=data2) #Load the latest data into the Index page of the Web Server  

#Retrieve a Summary of the latest results from the Database and decode it into a JSON Format
#This is included for a Mobile Application - but is not used in this project due to time constraints
@app.route("/summary")
def summary():
 db = MySQLdb.connect("localhost","pi","secret","IT715Project" )
 cursor = db.cursor()
 query = "select id, date, time, time2, temp, humidity, soil from temps ORDER BY id DESC LIMIT 1" #Get the latest date in the SQL Table
 cursor.execute(query)
 data2 = cursor.fetchall()
 fetchedData = json.dumps(data2) #Dump this data into a JSON Format
 d = json.JSONDecoder() #Decode this data into a JSON Format
 db.close()
 return fetchedData #Display this in a JSON Format

#Communicate to the Greenhouse Plants saying Hi
@app.route('/flicker')
def dynamic_page():
	led.led_flash() #Run the Flask Metho in the LED Python Script
	return render_template('hi.html') #Return a message saying you said hi to your plants

#Run the Webserver on Port 80 (HTTP Port) to ensure that a reverse proxy does not need to be used, and the website can be easily accessed
app.run(debug=True, host='0.0.0.0', port=80)
