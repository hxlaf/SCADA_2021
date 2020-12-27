#!/usr/bin/python3
import sys, os
import time
import smbus

#CONFIG PATH
lib_path = '/usr/etc/scada'
config_path = '/usr/etc/scada/config'

sys.path.append(lib_path)
sys.path.append(config_path)

from drivers import driver
import utils
import config
import redis

#Setting Up I2C Bus Connection 
bus = smbus.SMBus(3) ##Currently On Bus 3 with clock stretching 

#Setting up connectiion to Redis Server
Redisdata = redis.Redis(host='localhost', port=6379, db=0)
data = Redisdata.pubsub()
data.subscribe('raw_data')

#Local Dictionary for Sensor Period Count 
SensorList = config.get('Sensors')
last_sampled = {}
sample_period = {}
for key in config.get('Sensors'):
    sample_period[key] = SensorList.get(key).get('sample_period')
    last_sampled[key] = time.time()

#######Configure BNO055 IMU ########

#Defined IMU Constants
CONFIG_MODE= 0x00
IMU_MODE = 0x08
NDOF_MODE = 0x0C
POWER_NORMAL= 0x00
ACCEL_4G = 0x01
GYRO_2000_DPS = 0x00
MAGNETOMETER_20HZ = 0x05

#Defined IMU Registers
OPR_MODE_REG = 0x3D
PAGE_REG = 0x07
CALIBRATION_REG = 0x35
TRIGGER_REG = 0x3F
POWER_REG = 0x3E
ACC_CONFIG_REG = 0x08
MAG_CONFIG_REG = 0x09
GYRO_CONFIG_REG = 0x0A


def reset():
    #IMU IN CONFIG MODE
    bus.write_byte_data(0x28,OPR_MODE_REG,CONFIG_MODE)
    try:
        bus.write_byte_data(0x28,TRIGGER_REG,0X20)
    except OSError:
        pass
    time.sleep(0.7)
    

def setup():
    print("IMU SETTING UP")
    reset()
    bus.write_byte_data(0x28,POWER_REG,POWER_NORMAL)
    bus.write_byte_data(0x28,PAGE_REG,0x00)
    bus.write_byte_data(0x28,TRIGGER_REG,0x00)
    bus.write_byte_data(0x28,ACC_CONFIG_REG,ACCEL_4G)
    bus.write_byte_data(0x28,GYRO_CONFIG_REG,GYRO_2000_DPS)
    bus.write_byte_data(0x28,MAG_CONFIG_REG,MAGNETOMETER_20HZ)
    time.sleep(0.01)
    ##Setting IMU TO NDOF MODE
    bus.write_byte_data(0x28,OPR_MODE_REG,NDOF_MODE)
    time.sleep(0.01)


while True: 
    #for Sensors: <-- needs to be name of list of sensors
    # milliseconds = int(time()*1000)
    for sensorName in SensorList :
        if(time.time() - last_sampled[sensorName] > sample_period[sensorName] and float(sample_period[sensorName]) != 0.0):
            
            print('SENSOR NAME IS ' + sensorName + 'and its type is')
            print(type(sensorName))

            #Appending sensor name to sensor value for distinction in redis database
            key = '{}:{}'.format(sensorName, driver.read(sensorName))
            #Python String Method that makes everything lowercase
            key = key.lower()
            print(key)
            #Putting Sensor Data into redis channel
            Redisdata.publish('raw_data',key)
            last_sampled[sensorName] = time.time()