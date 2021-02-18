from flask import Flask, request
from flask_script import Manager
import RPi.GPIO as GPIO
import os

app = Flask(__name__)
manager = Manager(app)

@app.route('/switch_on', methods=['POST'])
def SwitchOn():
    if request.method == 'POST':
        os.system('bash /home/pi/RPi_Cam_Web_Interface/start.sh')
        return '<h1>Switch ON!</h1>'

@app.route('/switch_off', methods=['POST'])
def SwitchOff():
    if request.method == 'POST':
        os.system('bash /home/pi/RPi_Cam_Web_Interface/stop.sh')
        return '<h1>SWITCH OFF!</h1>'

@app.route('/light_on', methods=['POST'])
def LightOn():
    if request.method == 'POST':
        GPIO.setmode(GPIO.BCM)
	GPIO.setup(26,GPIO.OUT,initial=GPIO.HIGH)
	GPIO.output(26,GPIO.LOW)
        return '<h1>Light ON!</h1>'

@app.route('/light_off', methods=['POST'])
def LightOff():
    if request.method == 'POST':
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(26,GPIO.OUT,initial=GPIO.HIGH)
        GPIO.output(26,GPIO.HIGH)
        return '<h1>Light OFF!</h1>'

@app.route('/fire', methods=['GET'])
def Fire():
    if request.method == 'GET':
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(13,GPIO.OUT,initial=GPIO.LOW)
        GPIO.output(13,GPIO.HIGH)
        GPIO.cleanup()
        return '<h1>Fire!</h1>'

if __name__ == '__main__':
    	manager.run()
