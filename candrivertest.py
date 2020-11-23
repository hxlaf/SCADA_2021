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
import can
import canopen
from drivers import can_driver
import time

# # open a connection to the redis server where we will
# # be writing data
# #data = redis.Redis(host='localhost', port=6379, db=0)

# class CanDriver:
#     #this should take in channel and bustype?
#     def __init__(self):
#         self.network = canopen.Network()
#         # #eventually the following lines should take arguments from config
#         can_info = config.get('bus_info').get('CAN')
#         # TODO: SHOULD I HAVE A TRY CATCH HERE?  THAT WOULD ALERT PROGRAM THAT CANBUS NOT CONNECTED
#         self.network.connect(channel=can_info.get('bus_type'), bustype=can_info.get('bus_type'))
#         # TODO: this will eventually be a loop that goes through nodes' EDS's
#         self.network.add_node(1, lib_path + '/utils/eds-files/[nodeId=001]eds_eDrive150.eds')
        
#         #ensure nodes are connected
#         # self.network.scanner.search()
#         # time.sleep(1)
#         # print("Connected Nodes:")
#         # for node_id in self.network.scanner.nodes:
#         #     print("Found node %d!" % node_id)

#         allSensors = config.get('Sensors')
#         self.sdoDict = {}
#         for sensorName in allSensors:
#             sensorDict = allSensors.get(sensorName)
#             if sensorDict['bus_type'] == 'CAN':
#                 #DEBUG:
#                 # print(sensorName)
#                 # print(sensorDict)
#                 # print config.get('Sensors').get(sensorDict)
#                 self.sdoDict[sensorName] = self.configure_sdo(sensorName,sensorDict)
#                 #DEBUG:
#                 # print('sdoDict =')
#                 # print(sdoDict)
 

#     def __del__(self):
#         #UNCOMMENT THIS FOR WORKING VERSION
#         self.network.disconnect()

#     def read(self,sensorName):
#         #for now this is a redundant step, but if we use other CAN-subprotocols
#         #or other canOpen structures, we would want to do some decision making here
#         return self.read_sdo(sensorName)


#     def configure_sdo(self, sensorName, sensorDict):
#         #sensor name is composed of the node name and the value name
#         [nodeName, valueName] = sensorName.split('-')
#         #DEBUG:
#         # print(nodeName)
#         # print(valueName)
#         nodeNum = config.get('can_nodes').get(nodeName)
#         #finds node on network
#         node = self.network[nodeNum]

#         #creates SDO object that will communicate with the node
#         if sensorDict['secondary_address'] == None:
#             new_sdo = node.sdo[sensorDict['primary_address']]
#         else:
#             new_sdo = node.sdo[sensorDict['primary_address']][sensorDict['secondary_address'][0]]
#         return new_sdo



#     #using SDOs for now
#     def read_sdo(self,sensorName):
#         return self.sdoDict[sensorName].phys
        
#     #technically this should be done in intruction parser?
#     #using SDOs for now
#     def write_sdo(self,sensorName):
#         #dummy method contents
#         pass

#     def read_pdo(self,sensorName):
#         #dummy method contents
#         pass

#     #technically this should be done in intruction parser?
#     def write_pdo(self, sensorName):
#         #dummy method contents
#         pass

#end class definition

# #begin test procedures
driver = can_driver.CanDriver()
value = driver.read['motor_select_application']
print("Value of " + 'motor_select_application' + " is: ")
print(value)
# value = driver.read['motor_nmt_state']
# print("Value of " + 'motor_nmt_state' + " is: ")
# print(value)

#THIS PROCEDURE SHOULD ENABLE DRIVE MODE
#write value
driver.write['motor_select_application', 1]
#doing some nmt stuff
driver.write['motor_nmt_state', 'RESET']
time.sleep(1)

value = driver.read['motor_select_application']
print("Value of " + 'motor_select_application' + " is: ")
print(value)
# value = driver.read['motor_nmt_state']
# print("Value of " + 'motor_nmt_state' + " is: ")
# print(value)
# print ('TADA!!!')

#write value
driver.write['motor_select_application', 0]
#doing some nmt stuff
# driver.write['motor_nmt_state', 'RESET']
time.sleep(1)

value = driver.read['motor_select_application']
print("Value of " + 'motor_select_application' + " is: ")
print(value)
# value = driver.read['motor_nmt_state']
# print("Value of " + 'motor_nmt_state' + " is: ")
# print(value)
# print ('TADAx2!!!')