import sys, os
import utils
#import usr/etc/scada/config

class Driver:
    def __init__():

Redisdata = redis.Redis(host='localhost', port=6379, db=0)

 # Method to read from the sesnor objects depending on protocol                
    def read(Sensor)
    #make it look at the folder for what protocol to use
        if(Sensor.protocol == 'I2C'):
            data = i2c_sorter.read(Sensor)
        elif(Sensor.protocol =='CAN'):
            data = can_sorter.read(Sensor)
        elif(Sensor.protocol == 'USB'):
            data= usb_sorter.read(Sensor)
        else:
            return 'Sensor Protocol Not Found'
         #Redis Write Command 
        Redisdata.publish('data', data)
            
    #Write to sensor 
    def write(Sensor,Value)
        if(Sensor.protocol == 'I2C'):
            i2c_sorter.write(Sensor, Value)
        elif(Sensor.protocol =='CAN'):
            can_sorter.write(Sensor,Value)
        elif(Sensor.protocol == 'USB'):
            usb_sorter.write(Sensor,Value)
        else:
            return 'Sensor Protocol Not Found'

while True: 
    #for Sensors: <-- needs to be name of list of sensors
        if(time % Sensor.period == 0):
            read(Sensor)