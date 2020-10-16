#!/usr/bin/python3
import sys, os

lib_path = '/usr/etc/scada'
config_path = '/usr/etc/scada/config'

sys.path.append(lib_path)
sys.path.append(config_path)

import config # Config Py Class Where YAML File is extracted into cide
import redis

import utils
from utils import calibration
import user_cal

import time
import datetime

# TODO: reintroduce verbose logging

# Configure Redis interface
data = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
p = data.pubsub()
p.subscribe('Sensor_data')

#Performs Calibration on Raw Sensor Values
def execute(Sensor_val):
		
	#Retrieve Calibration Function From Yaml Configuration File
	calibration_func = config.get(Sensor_val(0)[1:-1].get(cal_function))

	#Replacing Input Targets x0,x1, etc w/ raw values for calibration calc
	for i in range(len(config.get(Sensor_val(0)[1:-1].get(input_targets))))
		calibration_func.replace("x"+i,Sensor_val[1][1:-1])
	
	return eval(calibration_func) 
	
	
		
def update():
	#publishes calibrated data to the calculated data channel
	data.publish('calculated_data', execute(p.get_message.split(":")))


while True:
	message = p.get_message()
	if message:
		update()
	else:
		time.sleep(0.1)



