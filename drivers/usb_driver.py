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
import usb.core
import usb.util
import time

allSensors = config.get('Sensors')
usbDevices = {}

for sensorName in allSensors:
    sensorDict = allSensors.get(sensorName)
    if sensorDict['bus_type'] == 'USB':
        usbDevices[sensorName] = (configure_sensor(sensorDict))


def write(sensorName, value):
    pass

def read(self,sensorName):
    pass

def configure_sensor(self, sensorName, sensorDict):
    vendorID = sensorDict.get('primary_address')
    productID = sensorDict.get('secondary_address')
    return usb.core.find(idVendor=vendorID, idProduct = productID)
    