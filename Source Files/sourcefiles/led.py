import RPi.GPIO as GPIO
import time

#Flash an LED for 4 seconds to say Hi to the plants
def led_flash():
	GPIO.setmode(GPIO.BOARD)
	GPIO.setwarnings(False) #Don't display any GPIO Warnings
	GPIO.setup(7,GPIO.OUT)
	GPIO.output(7,GPIO.HIGH)
	time.sleep(4)
	GPIO.output(7,GPIO.LOW)
	GPIO.cleanup()