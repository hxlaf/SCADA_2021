#!/usr/bin/python3

import sys, os

#Importing the config file
lib_path = '/usr/etc/scada'
config_path = '/usr/etc/scada/config'

sys.path.append(lib_path)
sys.path.append(config_path)


import config
import redis
import can
import utils
#importing messages.py from utils directory
from utils import messages

# open a connection to the redis server where we will
# be writing data
data = redis.Redis(host='localhost', port=6379, db=0)

#Python-Can Listener class
class Listener(can.Listener):
	# Part of the Python_can Listener class and called to hangdle the given message
	def on_message_received(self, msg):

		# infer the CANOpen protocol used and node id of sender
		#Calling a method in the messages class that returns function id
		# which is the protocol and the node id
		protocol, node_id = messages.get_info(msg)

#		if protocol == 'SDO-WRITE':
#			if len(msg.data) == 0:
#				return
#
#			# check the config file to find out name of node
#			try:
#				node = config.get('can_nodes').get(node_id)
#			except:
#				return
#
#			control_byte = msg.data[0]
#			index = msg.data[2] * 256 + msg.data[1]
#			subindex = msg.data[3]
#
#			if index == 0x3003:
#				temp = msg.data[5] * 256 + msg.data[4]
#				print(f"cell: {subindex} at temp: {temp}")
#				data.setex(f"pack1:temp:cell_{subindex}",60,temp)

		# if the protocol used is one of the four types
		# of PDOs (Process Data Objects), then log it
		if protocol in ['PDO-1', 'PDO-2', 'PDO-3', 'PDO-4']:

			_, pdo_number = protocol.split('-')

			# check the config file to find out name of node
			try:
				#Can Nodes in config YAML File (Motor, TSI, Pack 1 and Pack 2) and get the node id to store it
				# in the variable node
				node = config.get('can_nodes').get(node_id)
			except:
				return

			# check the config file to figure out expected
			# structure of the process data
			if pdo_number == '1':
				pdo_structure = config.get('process_data').get(node)
			else:
				pdo_structure = config.get('process_data').get('{}-{}'.format(node, pdo_number))

			# separate can message into bytes and write each one
			# to the redis server with its name as defined in the
			# config file

			pipe = data.pipeline()

			for index, byte in enumerate(msg.data, start=0):
				##### What does this line mean?
				key = '{}:{}'.format(node, pdo_structure[index])
				#Python String Method that makes everything lowercase
				key = key.lower()
				pipe.setex(key, 10, int(byte))

			data.publish('bus_data', key)
			pipe.execute()

if __name__ == "__main__":
	bus = utils.bus(config.get('bus_info'))
	notifier = can.Notifier(bus, [Listener()])

	for msg in bus:
		pass
