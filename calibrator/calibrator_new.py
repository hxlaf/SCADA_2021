#!/usr/bin/python3
import sys, os
import redis
import time
import datetime

#CONFIG PATH
lib_path = '/usr/etc/scada'
config_path = '/usr/etc/scada/config'

sys.path.append(lib_path)
sys.path.append(config_path)

import config 
import utils


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
    
    for key in config.get('Sensors').get(Sensor_val[0]).get('inputs'):
        calibration_func = calibration_func.replace(key,Sensor_val[1])
    
    output = eval(calibration_func)
    
    #Getting Precision Specificed for Sensor for Printing 
    precision = config.get('Sensors').get(Sensor_val[0]).get('precision')
    format_var = "{0:."+str(precision)+'f}'
    formatted_data= format_var.format(output)
    #Adding Value of Calibrated Sensor to Local Dictionary 
    last_calc_vals[Sensor_val[0]] = formatted_data
    return(formatted_data)

#Method to peform Calibration on virtual sensors 
def Virtual_execute(Sensor_val):
    calibration_func = config.get('Sensors').get(Sensor_val[0]).get('cal_function')
    for key in config.get('Sensors').get(Sensor_val[0]).get('inputs'):
        calibration_func = calibration_func.replace(key,str(last_calc_vals[config.get('Sensors').get(Sensor_val[0]).get('inputs').get(key)]))
    
    output = eval(calibration_func)
    
    precision = config.get('Sensors').get(Sensor_val[0]).get('precision')
    format_var = "{0:."+str(precision)+'f}'
    formatted_data= format_var.format(output)
    last_calc_vals[Sensor_val[0]] = formatted_data
    return(formatted_data)
            
#Method publishes calibrated data to the Calculated Data Redis Channel      
def update(sensor_key):
    split_key = sensor_key.split(":")
    print ("SPlit KEY : " + split_key[0])
    
    #Checking the Length of the inputs dictionary from YAML file
    #Bus Type (CAN & I2C) - Raw Sensor Calibration Method Called 
    #Else - Virtual Sensor Calibration Method Called 
    if config.get('Sensors').get(split_key[0])).get('bus_type') != 'VIRTUAL':
        data.publish('calculated_data', '{}:{}'.format(split_key[0], str(execute(split_key)) ))
    else:
        data.publish('calculated_data', '{}:{}'.format(split_key[0],str(Virtual_execute(split_key))))
        

#Listening to the Calculated Data Channel for New Messages 
while True:
    message = p.get_message() 
    if (message and (message['data'] != 1 )):
        update(message['data'])
    else:
        time.sleep(0.1)



