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
import redis
import i2c_sorter
import can_driver


#Setting up connectiion to Redis Server
Redisdata = redis.Redis(host='localhost', port=6379, db=0)
data = Redisdata.pubsub()
data.subscribe('Sensor_data')

#Local Dictionary for Sensor Period Count 
SensorList = config.get('Sensors')
last_sampled = {}
sample_period = {}
for key in config.get('Sensors'):
    sample_period[key] = SensorList.get(key).get('sample_period')
    last_sampled[key] = time.time()


#set up CAN bus connection
os.system('ip link set can0 down')
os.system('ip link set can0 up type can bitrate 125000')
can_drive = can_driver.CanDriver()

# Method to read from the sesnor objects depending on protocol                
def read(Sensor):
#make it look at the folder for what protocol to use
    sensor_protocol = SensorList.get(str(Sensor)).get('bus_type')
    if(sensor_protocol == 'I2C'):
        data = i2c_sorter.read(Sensor)
    elif(sensor_protocol =='CAN'):
        data = can_drive.read(Sensor)
    #elif(sensor_protocol == 'USB'):
        #data= usb_sorter.read(Sensor)
    elif(sensor_protocol == 'VIRTUAL'):
        data= 0
    else:
        return 'Sensor Protocol Not Found'
        #Redis Write Command 
    return data

##Shouldn't this be in Instruction parser???

#Write to sensor 
def write(Sensor,Value):
    sensor_protocol = SensorList.get(str(Sensor)).get('bus_type')
    if(sensor_protocol == 'I2C'):
        i2c_sorter.write(Sensor, Value)
#     elif(sensor_protocol =='CAN'):
#         can_sorter.write(Sensor,Value)
#     elif(sensor_protocol == 'USB'):
#         usb_sorter.write(Sensor,Value)
    else:
        return 'Sensor Protocol Not Found'


while True: 
    #for Sensors: <-- needs to be name of list of sensors
    # milliseconds = int(time()*1000)
    for sensorName in SensorList :
        if(time.time() - last_sampled[sensorName] > sample_period[sensorName]):
            #Appending sensor name to sensor value for distinction in redis database
            key = '{}:{}'.format(sensorName, read(sensorName))
            #Python String Method that makes everything lowercase
            key = key.lower()
            print(key)
            #Putting Sensor Data into redis channel
            Redisdata.publish('Sensor_data',key)
            last_sampled[sensorName] = time.time()