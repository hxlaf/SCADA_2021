import sys, os

#Importing the config file
lib_path = '/usr/etc/scada'
config_path = '/usr/etc/scada/config'

sys.path.append(lib_path)
sys.path.append(config_path)

import config
import redis
import time

class SensorEmulator():
    def __init__(self, configDict):
        self.period = configDict.get('data_period')
        self.periodStart = time.time()
        pass

    def getValue(self):
        return self.calculateValue(time.time()-self.periodStart)
    
    def calculateValue(self, timeElapsed):
        pass
    

class ConstantEmulator(SensorEmulator):
    def __init__(self, configDict):
        super().__init__(configDict)

class SineEmulator(SensorEmulator):
    def __init__(self, configDict):
        super().__init__(configDict)

class RampEmulator(SensorEmulator):
    def __init__(self, configDict):
        super().__init__(configDict)

class CycleEmulator(SensorEmulator):
    def __init__(self, configDict):
        self.values = configDict.get('data_values')
        super().__init__(configDict)

    def calculateValue(self, timeElapsed):
        index = int((timeElapsed/self.period)*len(values))
        return self.values[index]

def read(sensorName):
    return emulators[sensorName].getValue()
        
def write(sensorName, value):
    emulators[sensorName].currValue = value

def configure_emulator(sensorDict):
    if sensorDict.get('data_pattern') == 'CYCLE':
        return CycleEmulator(sensorDict)
    else:
        return None 

allSensors = config.get('Sensors')
emulators = {}

for sensorName in allSensors:
    sensorDict = allSensors.get(sensorName)
    if sensorDict['bus_type'] == 'EMULATED':
        emulators[sensorName] = (configure_emulator(sensorDict))


