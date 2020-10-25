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
    calibration_func = __config.get('Sensors').get(Sensor_val[0][1:-1]).get('cal_function')
    
    for key in __config.get('Sensors').get(Sensor_val[0][1:-1]).get('inputs'):
    #    print("Key INPUT" + key)
    #    print("Value of Key: " + __config.get('Sensors').get(Sensor_val[0][1:-1]).get('inputs').get(key))
        calibration_func = calibration_func.replace(key,Sensor_val[1][1:-1])
    
   # print(calibration_func)
    output = eval(calibration_func)
    #last_calc_vals[Sensor_val[0][1:-1]] = output
    precision = __config.get('Sensors').get(Sensor_val[0][1:-1]).get('precision')
    last_calc_vals[Sensor_val[0][1:-1]] = round(int(output),precision)
    return(output)

#Method to peform calibration function on virtual sensors 
def Virtual_execute(Sensor_val):
    calibration_func = __config.get('Sensors').get(Sensor_val[0][1:-1]).get('cal_function')
    for key in __config.get('Sensors').get(Sensor_val[0][1:-1]).get('inputs'):
        calibration_func = calibration_func.replace(key,str(last_calc_vals[__config.get('Sensors').get(Sensor_val[0][1:-1]).get('inputs').get(key)]))
    output = eval(calibration_func)
    
    precision = __config.get('Sensors').get(Sensor_val[0][1:-1]).get('precision')
    last_calc_vals[Sensor_val[0][1:-1]] = round(int(output),precision)
    #Added for Debugging
    #print(last_calc_vals)
    return(output)
			
#Method publishes calibrated data to the calculated data channel		
def update(sensor_key):
    #publishes calibrated data to the calculated data channel
    split_key = sensor_key.split(":")
    #print("SPLIT_KEY " + split_key[0][1:-1])
    if len((__config.get('Sensors').get(split_key[0][1:-1])).get('input_targets')) == 1:
        #print ("LEN IS WORKING!")
        #print('calculated_data', '{}:{}'.format(split_key[0], execute(split_key)))
        r.publish('calculated_data', '{}:{}'.format(split_key[0], str('{' + str(execute(split_key)) + '}')))
    else:
        #print("IM IN ELSE")
        #print("Virtual Sensors" + '{}:{}'.format(split_key[0], Virtual_execute(split_key)))
        r.publish('calculated_data', '{}:{}'.format(split_key[0],str('{'+ str(Virtual_execute(split_key)) + '}')))
		

while True:
	message = p.get_message() 
	if message:
		update(message['data'])
	else:
		time.sleep(0.1)



