import sys, os

#Importing the config file
lib_path = '/usr/etc/scada'
config_path = '/usr/etc/scada/config'
#this is temporary, just for testing
local_path = '../utils'

sys.path.append(lib_path)
sys.path.append(config_path)
sys.path.append(local_path)

import config
import redis
import usb
import time

class USBSensor():
    def __init__(self, configDict):
        self.vendorID

    def calculateValue(self, timeElapsed):
        pass

allSensors = config.get('Sensors')
emulators = {}

for sensorName in allSensors:
    sensorDict = allSensors.get(sensorName)
    if sensorDict['bus_type'] == 'USB':
        emulators[sensorName] = (configure_emulator(sensorDict))


def write(sensorName, value):
    

def read(self,sensorName):
    #dummy method contents
    pass

def configure_sensor(self, sensorName, sensorDict):
    
    