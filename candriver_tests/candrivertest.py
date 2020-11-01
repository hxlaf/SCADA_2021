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
import can
import canopen
import database

# open a connection to the redis server where we will
# be writing data
data = redis.Redis(host='localhost', port=6379, db=0)

class CanDriver:
    #this should take in channel and bustype?
    def __init__(self):
        self.network = canopen.Network()
        # #eventually the following lines should take arguments from config
        # self.network.connect(channel='can0', bustype='socketcan')
        # #this will eventually be a loop that goes through nodes
        node = self.network.add_node(1, lib_path + '/utils/eds-files/[nodeId=001]eds_eDrive150.eds')
        # self.network.scanner.search()
        # time.sleep(1)
        # #this is for testing only
        # for node_id in self.network.scanner.nodes:
        #     print("Found node %d!" % node_id)
        sdoDict = {}
        allSensors = config.get('Sensors')
        for sensorName in allSensors:
            sensorDict = allSensors.get(sensorName)
            if sensorDict['bus_type'] == 'CAN':
                print(sensorName)
                print(sensorDict)
                # print config.get('Sensors').get(sensorDict)
                #TODO: some way to determine node object beforehand
                    #we only have one right now for testing, so it doesn't matter
                sdoDict[sensorName] = self.configure_sdo(sensorName,sensorDict)
                print('sdoDict =')
                print(sdoDict)
 
    def __del__(self):
        #UNCOMMENT THIS FOR WORKING VERSION
        # self.network.disconnect()
        pass

    def configure_sdo(self, sensorName, sensorDict):
        #sensor name is composed of the node name and the value name
        [nodeName, valueName] = sensorName.split('-')
        print(nodeName)
        print(valueName)
        nodeNum = config.get('can_nodes').get(nodeName)
        node = self.network[nodeNum]

        if sensorDict['secondary_address'] == None:
            new_sdo = node.sdo[sensorDict['primary_address']]
        else:
            new_sdo = node.sdo[sensorDict['primary_address']][sensorDict['secondary_address'][0]]
        return new_sdo

    #using SDOs for now
    def read_sdo(self,primAddress, secAddress):
        #dummy method contents
        pass
        
    #technically this should be done in intruction parser?
    #using SDOs for now
    def write_sdo(self,primAddress, secAddress):
        #dummy method contents
        pass

    def read_pdo(self,primAddress, secAddress):
        #dummy method contents
        pass

    #technically this should be done in intruction parser?
    def write_pdo(self, primAddress, secAddress):
        #dummy method contents
        pass
#end class definition

#begin test procedures
driver = CanDriver()
print(database.getData(sensor_id = 'test_sensor'))

