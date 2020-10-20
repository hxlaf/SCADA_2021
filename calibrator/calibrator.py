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

# Configure Redis interface For Raw Sensors Data
data = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
p = data.pubsub()
p.subscribe('Sensor_data')


#Local Dictionary storing values of Calibrated Sensors used for Virtual Sensors
last_calc_vals = {}

#Performs Calibration on Raw Sensor Values
def execute(Sensor_val):
		
	#Retrieve Calibration Function From Yaml Configuration File
	calibration_func = config.get('Sensors').get(Sensor_val[0]).get('cal_function')

	#Replacing Input Targets x0,x1, etc w/ raw values for calibration calc
	calibration_func = calibration_func.replace("x0",Sensor_val[1])
	output = eval(calibration_func)
	last_calc_vals[Sensor_val[0]] = output
	return(output)

#Method to peform calibration function on virtual sensors 
def Virtual_execute(Sensor_val):
    calibration_func = __config.get('Sensors').get(Sensor_val[0][1:-1]).get('cal_function')
    for i in range(len(__config.get('Sensors').get(Sensor_val[0][1:-1]).get('input_targets'))):
        calibration_func = calibration_func.replace("x"+str(i),str(last_calc_vals[__config.get('Sensors').get(Sensor_val[0][1:-1]).get('input_targets')[i]])) #<--- this sensor_val thing needs to change
    output = eval(calibration_func)
    last_calc_vals[Sensor_val[0][1:-1]] = output
    return(output)
			
#Method publishes calibrated data to the calculated data channel		
def update(sensor_key):
     split_key = sensor_key.split(":")
    if len((__config.get('Sensors').get(split_key[0][1:-1])).get('input_targets')) == 1:
        data.publish('calculated_data', '{}:{}'.format(split_key[0], str('{' + str(execute(split_key)) + '}')))
    else:
    	data.publish('calculated_data', '{}:{}'.format(split_key[0],str('{'+ str(Virtual_execute(split_key)) + '}')))
		

while True:
	message = p.get_message() 
	if message:
		update(message['data'])
	else:
		time.sleep(0.1)



