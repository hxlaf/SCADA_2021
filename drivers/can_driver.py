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
# from utils import database
import time



# open a connection to the redis server where we will
# be writing data
#data = redis.Redis(host='localhost', port=6379, db=0)

class CanDriver:
    #this should take in channel and bustype?
    def __init__(self):
        self.network = canopen.Network()
        # #eventually the following lines should take arguments from config
        can_info = config.get('bus_info').get('CAN')
        # TODO: SHOULD I HAVE A TRY CATCH HERE?  THAT WOULD ALERT PROGRAM THAT CANBUS NOT CONNECTED
        self.network.connect(channel=can_info.get('channel'), bustype=can_info.get('bus_type'))
        # TODO: this will eventually be a loop that goes through nodes' EDS's
        self.network.add_node(1, lib_path + '/utils/eds-files/[nodeId=001]eds_eDrive150.eds')
        
        #ensure nodes are connected
        # self.network.scanner.search()
        # time.sleep(1)
        # print("Connected Nodes:")
        # for node_id in self.network.scanner.nodes:
        #     print("Found node %d!" % node_id)

        allSensors = config.get('Sensors')
        self.sdoDict = {}
        for sensorName in allSensors:
            sensorDict = allSensors.get(sensorName)
            if sensorDict['bus_type'] == 'CAN':
                #DEBUG:
                print(sensorName)
                print(sensorDict)
                # print config.get('Sensors').get(sensorDict)
                if 'nmt' not in sensorName:
                    self.sdoDict[sensorName] = self.configure_sdo(sensorName,sensorDict)
                #DEBUG:
                # print('sdoDict =')
                # print(sdoDict)
 

    def __del__(self):
        #UNCOMMENT THIS FOR WORKING VERSION
        self.network.disconnect()

    def read(self,sensorName):
        #for now this is a redundant step, but if we use other CAN-subprotocols
        #or other canOpen structures, we would want to do some decision making here
        print('SENSOR NAME IS ' + sensorName + 'and its type is')
        print(type(sensorName))
        try:
            # if 'nmt' in sensorName:
            if sensorName.find('nmt') != -1:
                return self.read_nmt(sensorName)
            else:
                return self.read_sdo(sensorName)
        except OSError:
            return None

    def write(self,sensorName, value):
        #for now this is a redundant step, but if we use other CAN-subprotocols
        #or other canOpen structures, we would want to do some decision making here
        try:
            if 'nmt' in sensorName:
                self.write_nmt(sensorName, value)
            else: 
                self.write_sdo(sensorName, value)
        except OSError:
            pass

    #using SDOs for now
    def read_sdo(self,sensorName):
        return self.sdoDict[sensorName].phys

    def read_nmt(self,sensorName):
        #sensor name is composed of the node name and the value name
        [nodeName, *valueName] = sensorName.split('_')
        #get node ID from config
        nodeNum = config.get('can_nodes').get(nodeName)
        #select node on network
        node = self.network[nodeNum]

        if 'state' in sensorName:
            return node.nmt.state
        
    #using SDOs for now
    def write_sdo(self,sensorName, value):
        sdoDict[sensorName].phys = value

    def write_nmt(self,sensorName, value):
        #sensor name is composed of the node name and the value name
        [nodeName, *valueName] = sensorName.split('_')
        #get node ID from config
        nodeNum = config.get('can_nodes').get(nodeName)
        #select node on network
        node = self.network[nodeNum]

        if 'state' in sensorName:
            node.nmt.state(value)

    def read_pdo(self,sensorName):
        #dummy method contents
        pass
    
    #write_pdo method is not applicable because it's only used to get data from devices

    def configure_sdo(self, sensorName, sensorDict):
        #sensor name is composed of the node name and the value name
        [nodeName, *valueName] = sensorName.split('_')
        #get node ID from config
        nodeNum = config.get('can_nodes').get(nodeName)
        #select node on network
        node = self.network[nodeNum]

        #creates SDO object that will communicate with the sensor
        if sensorDict['secondary_address'] == None:
            new_sdo = node.sdo[sensorDict['primary_address']]
        else:
            new_sdo = node.sdo[sensorDict['primary_address']][sensorDict['secondary_address']]
        return new_sdo
    