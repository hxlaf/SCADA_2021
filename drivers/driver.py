#!/usr/bin/python3
import sys, os
import time

#CONFIG PATH
lib_path = '/usr/etc/scada'
config_path = '/usr/etc/scada/config'

sys.path.append(lib_path)
sys.path.append(config_path)

import utils
import config
import i2c_driver
import can_driver

SensorList = config.get('Sensors')

#set up CAN bus connection
os.system('ip link set can0 down')
os.system('ip link set can0 up type can bitrate 125000')
can_drive = can_driver.CanDriver()

#Set RTC Time to Sys Time 
#os.system ()


# Method to read from the sesnor objects depending on protocol                
def read(Sensor):
#make it look at the folder for what protocol to use
    sensor_protocol = SensorList.get(str(Sensor)).get('bus_type')
    if(sensor_protocol == 'I2C'):
        data = i2c_driver.read(Sensor)
    elif(sensor_protocol =='CAN'):
        data = can_drive.read(Sensor)
    #elif(sensor_protocol == 'USB'):
        #data= usb_sorter.read(Sensor)
    elif(sensor_protocol == 'VIRTUAL'):
        data= 0
    else:
        return 'Sensor Protocol Not Found'
        #Redis Write Command 

    if data == None:
        data = 'BUS ERROR'
    return data


#Write to sensor 
def write(Sensor,Value):
    sensor_protocol = SensorList.get(str(Sensor)).get('bus_type')
    if(sensor_protocol == 'I2C'):
        i2c_driver.write(Sensor, Value)
    elif(sensor_protocol =='CAN'):
        can_drive.write(Sensor,Value)
#     elif(sensor_protocol == 'USB'):
#         usb_sorter.write(Sensor,Value)
    else:
        return 'Sensor Protocol Not Found'


# while True: 
#     #for Sensors: <-- needs to be name of list of sensors
#     # milliseconds = int(time()*1000)
#     for sensorName in SensorList :
#         if(time.time() - last_sampled[sensorName] > sample_period[sensorName] and float(sample_period[sensorName]) != 0.0):
#             #Appending sensor name to sensor value for distinction in redis database
#             key = '{}:{}'.format(sensorName, read(sensorName))
#             #Python String Method that makes everything lowercase
#             key = key.lower()
#             print(key)
#             #Putting Sensor Data into redis channel
#             Redisdata.publish('raw_data',key)
#             last_sampled[sensorName] = time.time()