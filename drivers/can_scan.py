#!/usr/bin/python3
import sys, os
import time

#Importing the config file
lib_path = '/usr/etc/scada'
config_path = '/usr/etc/scada/config'
#this is temporary, just for testing
local_path = '../utils'

sys.path.append(lib_path)
sys.path.append(config_path)
sys.path.append(local_path)

from drivers import can_driver

cd = can_driver.CanDriver()
network = cd.network

#ensure nodes are connected
network.scanner.search()
time.sleep(1)
print("Connected Nodes:")
for node_id in network.scanner.nodes:
    print("Found node %d!" % node_id)