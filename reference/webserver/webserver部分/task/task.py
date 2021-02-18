
import RPi.GPIO as GPIO
import json
import math
import requests
import sys
from time import sleep
import os

class Task_Class:

    def HTF(self):
        IP = "192.168.0.54"        # The IP of the machine hosting your influxdb instance
        DB = "openhab_db"               # The database to write to, has to exist
        USER = "openhab"             # The influxdb user to authenticate with
        PASSWORD = "raspberry"  # The password of that user
        #TIME = 1                  # Delay in seconds between two consecutive updates
       # STATUS_MOD = 5            # The interval in which the updates count will be printed to your console
        while 1:
            bits_humidity=[]
            bits_temperature=[]
            bits_fire=[]
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(17, GPIO.OUT,initial=GPIO.HIGH)
            GPIO.setup(27, GPIO.OUT,initial=GPIO.LOW)
            GPIO.setup(22, GPIO.IN)
            sleep(0.04)
            GPIO.output(17, GPIO.LOW)
            sleep(0.04)
            GPIO.output(17, GPIO.HIGH)
            for i in range(12):
                GPIO.output(27, GPIO.HIGH)
                sleep(0.01)
                bit_temperature=(GPIO.input(22))
                bits_temperature.append(bit_temperature)
                sleep(0.01)
                GPIO.output(27, GPIO.LOW)
                sleep(0.01)
            for i in range(12):
                GPIO.output(27, GPIO.HIGH)
                sleep(0.01)
                bit_humidity=(GPIO.input(22))
                bits_humidity.append(bit_humidity)
                sleep(0.01)
                GPIO.output(27, GPIO.LOW)
                sleep(0.01)
            for i in range(4):
                GPIO.output(27, GPIO.HIGH)
                sleep(0.01)
                bit_fire=(GPIO.input(22))
                bits_fire.append(bit_fire)
                sleep(0.01)
                GPIO.output(27, GPIO.LOW)
                sleep(0.01)
            humidity=((8*bits_humidity[0]+4*bits_humidity[1]+2*bits_humidity[2]+bits_humidity[3])*10+\
                (8*bits_humidity[4]+4*bits_humidity[5]+2*bits_humidity[6]+bits_humidity[7])+\
                (8*bits_humidity[8]+4*bits_humidity[9]+2*bits_humidity[10]+bits_humidity[11])*0.1)
            temperature=10*((8*bits_temperature[0]+4*bits_temperature[1]+2*bits_temperature[2]+bits_temperature[3])*10+\
                (8*bits_temperature[4]+4*bits_temperature[5]+2*bits_temperature[6]+bits_temperature[7])+\
                (8*bits_temperature[8]+4*bits_temperature[9]+2*bits_temperature[10]+bits_temperature[11])*0.1)
            if bits_fire[3]==0:
            	os.system('http GET 127.0.0.1:5000/fire')
            GPIO.cleanup()
            v1 = 'temp_wave value=%d' % temperature
            v2 = 'humi_wave value=%d' % humidity
            r1 = requests.post("http://%s:8086/write?db=%s" %(IP, DB), auth=(USER, PASSWORD), data=v1)
            r2 = requests.post("http://%s:8086/write?db=%s" %(IP, DB), auth=(USER, PASSWORD), data=v2)
            print(['POST Success!',temperature,humidity])
        return(1)
