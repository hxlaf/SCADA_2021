#!/usr/bin/python3
import sys, os
import time

#CONFIG PATH
lib_path = '/usr/etc/scada'
config_path = '/usr/etc/scada/config'

sys.path.append(lib_path)
sys.path.append(config_path)

from drivers import driver
import utils
import config
import redis

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


while True: 
    #for Sensors: <-- needs to be name of list of sensors
    # milliseconds = int(time()*1000)
    for sensorName in SensorList :
        if(time.time() - last_sampled[sensorName] > sample_period[sensorName] and float(sample_period[sensorName]) != 0.0):
            #Appending sensor name to sensor value for distinction in redis database
            key = '{}:{}'.format(sensorName, driver.read(sensorName))
            #Python String Method that makes everything lowercase
            key = key.lower()
            print(key)
            #Putting Sensor Data into redis channel
            Redisdata.publish('raw_data',key)
            last_sampled[sensorName] = time.time()