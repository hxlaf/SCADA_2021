import sys, os

#Importing the config file
lib_path = '/usr/etc/scada'
config_path = '/usr/etc/scada/config'

sys.path.append(lib_path)
sys.path.append(config_path)

import config
import redis
import can
import canopen

# open a connection to the redis server where we will
# be writing data
data = redis.Redis(host='localhost', port=6379, db=0)

class CanSorter:

    def __init__:
        network = canopen.Network()
        #eventually this should take arguments from config
        network.connect(channel='can0', bustype='socketcan')

    def configure(sensorDict)

    #using SDOs for now
    def read_sdo(primAddress, secAddress):

    #technically this should be done in intruction parser?
    #using SDOs for now
    def write_sdo(primAddress, secAddress):




    def read_pdo(primAddress, secAddress):

    #technically this should be done in intruction parser?
    def write_pdo(primAddress, secAddress):