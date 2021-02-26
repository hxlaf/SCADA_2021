import sys, os

#Importing the config file
lib_path = '/usr/etc/scada'
config_path = '/usr/etc/scada/config'

sys.path.append(lib_path)
sys.path.append(config_path)

import config
import redis
import time

FullSensorDict = config.get('Sensors')
emulators = {}

for sensorDict in FullSensorDict:
    if sensorDict['bus_type'] == 'EMULATED':
        emulatorObjs.append(configure_emulator(sensorDict))

def read(sensorName):
    return emulators[sensorName].getValue()
        
def write(sensorName, value):
    emulators[sensorName].currValue = value

def configure_emulator(sensorName, sensorDict):
    if sensor_dict.get('data_pattern') == 'CYCLE':
        return CycleEmulator(sensorDict)
    else:
        return None

class SensorEmulator():
    def __init__(self, configDict):
        self.period = configDict.get('sample_period')
        self.periodStart = time.time()
        pass

    def getValue(self):
        return self.calculateValue(time.time()-self.periodStart)
    
    def calculateValue(self, timeElapsed):
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
        self.values = configDict.get('data_values')

    def calculateValue(self, timeElapsed):
        index = int((timeElapsed/self.period)*len(values))
        return self.values[index]
        