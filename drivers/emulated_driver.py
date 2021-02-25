import sys, os

#Importing the config file
lib_path = '/usr/etc/scada'
config_path = '/usr/etc/scada/config'

sys.path.append(lib_path)
sys.path.append(config_path)

import config
import redis
import time

emulatedSensorDict = config.get('Emulated_Sensors')
emulatorObjs = {}


def read(sensorName):
    return emulatedSensorDict[sensorName].currValue()
        
def write(sensorName, value):
    emulatorObjs[sensorName].currValue = value

def configure_emulator(sensorName, sensorDict):
    #sensor name is composed of the node name and the value name
    pass

class SensorEmulator():
    def __init__(self, configDict):
        self.currValue = 0
        pass

class ConstantEmulator(SensorEmulator):
    def __init__(self, configDict):
        pass

class SineEmulator(SensorEmulator):
    def __init__(self, configDict):
        pass

class RampEmulator(SensorEmulator):
    def __init__(self, configDict):
        pass

class CycleEmulator(SensorEmulator):
    def __init__(self, configDict):
        pass