from flask import Flask, request
from flask_script import Manager
import os

app = Flask(__name__)
manager = Manager(app)

@app.route('/switch_on', methods=['POST'])
def get():
    if request.method == 'POST':
        os.system('bash /home/pi/RPi_Cam_Web_Interface/start.sh')
        return '<h1>Switch ON!</h1>'

@app.route('/switch_off', methods=['POST'])
def post():
    if request.method == 'POST':
        os.system('bash /home/pi/RPi_Cam_Web_Interface/stop.sh')
        return '<h1>SWITCH OFF!</h1>'

if __name__ == '__main__':
    manager.run()
