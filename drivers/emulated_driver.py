import sys, os

#Importing the config file
lib_path = '/usr/etc/scada'
config_path = '/usr/etc/scada/config'

sys.path.append(lib_path)
sys.path.append(config_path)

import config
import redis
import time
import math

class SensorEmulator():
    def __init__(self, configDict):
        self.period = configDict.get('data_period')
        self.periodStart = time.time()
        self.values = configDict.get('data_values')

    def getValue(self):
        # calculate time into period
        timeElapsed = time.time()-self.periodStart
        # check to see if in new period
        if timeElapsed > self.period:
            #reset periodStart and timeElapsed for new period
            self.periodStart = time.time()
            timeElapsed = timeElapsed - self.period
        self.currValue = self.calculateValue(timeElapsed)
        return self.currValue
    
    def calculateValue(self, timeElapsed):
        return None
    

class ConstantEmulator(SensorEmulator):
    def __init__(self, configDict):
        super().__init__(configDict)
        self.currValue = self.values
    
    def calculateValue(self,timeElapsed):
        return self.currValue

class SineEmulator(SensorEmulator):
    def __init__(self, configDict):
        super().__init__(configDict)

    def calculateValue(self,timeElapsed):
        return math.sin(2*math.pi/self.period * timeElapsed)
    

class RampEmulator(SensorEmulator):
    def __init__(self, configDict):
        super().__init__(configDict)
        self.slope = 2 * (self.values[1] - self.values[0])/self.period

    # generates a value for the "triangle wave" form at a given time int
    def calculateValue(self,timeElapsed):
        # second half of period going down
        if timeElapsed > 0.5 * self.period:
            return self.values[1] - self.slope*(timeElapsed - self.period/2)
        # first half of period going down
        return self.values[0] + self.slope*timeElapsed

class CycleEmulator(SensorEmulator):
    def __init__(self, configDict):
        super().__init__(configDict)

    def calculateValue(self, timeElapsed):
        index = int((timeElapsed/self.period)*len(self.values))
        return self.values[index]

def read(sensorName):
    return emulators[sensorName].getValue()
        
def write(sensorName, value):
    emulators[sensorName].currValue = value

def configure_emulator(sensorDict):
    pattern = sensorDict.get('data_pattern')
    print('sensor called' + sensorDict['var_name'] + 'has pattern_type' + pattern)
    if pattern == 'CYCLE':
        return CycleEmulator(sensorDict)
    elif pattern == 'SINE':
        return SineEmulator(sensorDict)
    elif pattern == 'RAMP':
        return RampEmulator(sensorDict)
    elif pattern == 'CONSTANT':
        return ConstantEmulator(sensorDict)
    else:
        print('sensor called' + sensorDict['var_name'] + 'could not be configured')
        return None 

allSensors = config.get('Sensors')
emulators = {}

for sensorName in allSensors:
    sensorDict = allSensors.get(sensorName)
    if sensorDict['bus_type'] == 'EMULATED':
        emulators[sensorName] = (configure_emulator(sensorDict))


