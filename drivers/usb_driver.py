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

def write(sensorName, value):
    pass

def read(sensorName):
    usbDevices[sensorName].read()
    pass

def configure_sensor(sensorName, sensorDict):
    vendorID = sensorDict.get('primary_address')
    productID = sensorDict.get('secondary_address')
    
    #stuff from pyusb github example
    dev =  usb.core.find(idVendor=vendorID, idProduct = productID)
    if dev is None:
        raise ValueError('Device not found')
    dev.set_configuration()
    cfg = dev.get_active_configuration()
    intf = cfg[(0,0)]

    ep = usb.util.find_descriptor(
        intf,
        # match the first OUT endpoint
        custom_match = \
        lambda e: \
            usb.util.endpoint_direction(e.bEndpointAddress) == \
            usb.util.ENDPOINT_OUT)

    return dev

for sensorName in allSensors:
    sensorDict = allSensors.get(sensorName)
    if sensorDict['bus_type'] == 'USB':
        usbDevices[sensorName] = configure_sensor(sensorDict)
        print('just added usb device called' + sensorName)