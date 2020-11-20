# This Python Script uses the Temperture Sensor, Soil Moisture Sensor and the Raspbery Pi Camaera to get the latest readings
# and inserts this into the IT715 SQL Database on the Raspberry Pi to be read by the Webserver

import MySQLdb
import adafruit_dht
import board
import datetime
import time
from picamera import PiCamera
import RPi.GPIO as GPIO

soilPin = 25 #Set the SoilPin (using BOARD)

GPIO.setup(soilPin, GPIO.IN) #Set the SoilPin as an Input (Receiving data)

camera = PiCamera() #Create an instance of the Pi Camera
camera.rotation = 180 # Change the rotation of the Pi Camera's Image by 180 Degrees so it is upright

dhtDevice = adafruit_dht.DHT11(board.D23) #Temperture Sensor
db = MySQLdb.connect("localhost","pi","secret","IT715Project" ) #Database Connection
cursor = db.cursor() #Database Cursor
try:
	while True:
		x = datetime.datetime.now() #Get Date and Time
		temp = dhtDevice.temperature #Get Temp
		hum = dhtDevice.humidity #Get Humidity
		soil = GPIO.input(soilPin) #Check whether there is any water in the soil
		print('Temp: {0} Hum: {1}%'.format(temp,hum)) # Write to Console Screen current Temp & Humidity
		if(soil):
			print('No Water Detected in Soil') #Print No Water Detected (1 | True)
		else:
			print('Water Detected in Soil') #Print water detected (0 | False)
		camera.start_preview() #Turn the camera on
		time.sleep(5)
		camera.capture('/home/pi/app/sourcefiles/static/img/photo.jpg') #Save the image in the Cameras focus/preview to the server image
		camera.stop_preview() #Turn the camera off
		print('Photo Captured') #Print successful photo
		query = "insert into temps (date, time, time2, temp, humidity, soil)"\
		+ "values('{}', {}, {}, {}, {}, {})"\
		.format(x.strftime("%d %B %Y"), x.strftime("%H"), x.strftime("%M"), temp, hum, soil) #Insert into the database latest values
		try:
			cursor.execute(query)
			db.commit() #Commit Changes
			print('Sent to Database') #Send to Database Message
			print('-------------------------------------------------------------------------')
		except:
			print(db) #Print Error Message
			db.rollback() #Uncommit Changes
			print(db) #Print Error Message
			print("---------ERROR---------") #Error Sending to Database
		print('-------------------------------------------------------------------------')
		time.sleep(1800) #Wait 30 minutes before getting latest readings
except KeyboardInterrupt: #If Keyboard Ctrl C pressed
	db.close() #Close the Database Connection
	print("Database Connection Closed")
	print("Application Closed")
