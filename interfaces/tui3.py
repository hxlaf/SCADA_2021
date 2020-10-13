#!/usr/bin/python3
import sys, os

# scada_path = os.environ['SCADA_PATH']
scada_path = '/usr/etc/scada'
config_path = '/usr/etc/scada/config'

sys.path.append(scada_path)
sys.path.append(config_path)

from blessed import Terminal
term = Terminal()

import config
import redis
import time

data = redis.Redis(host='localhost', port=6379, db=0)

# Retrieveing Display from config.yaml -TSI -- iriwn added this
columns = config.get('Display')

def print_column(data, label, x=0, y=0):
	
	print(term.move_y((term.height // 2) - len(data) // 2 ))

	col = ''

	col += term.move_x(x)
	col += term.bold_underline(label)
	col += term.move_down(1)

	for name, value in data:
		col += term.move_x(x)
		col += '{}'.format(name)
		col += term.move_x(x + 20)
		col += '{}'.format(value)
		col += term.move_down(1)
	print(col)

def update():
	print(term.clear())
	

	# motor_data = []
	labelCol = []
	dataCol = []
	Sensors = config.get('Sensors')

	for key in Sensors:

		target = Sensors.get(key).get('data_target')
		if target != None:
			value = data.get(target)
			value = str(value)
			value = str(value)
			value = value.replace("b'", "")
			value = value.replace("'", "")
			unit = Sensors.get(key).get('unit')
			unit = str(unit)
			targetName = str(target)
			value += " " + unit
			dataCol.append((target, value))

	print_column(labelCol, 'All the Simulated Data', 10,0)



while True:
	update()
	time.sleep(0.5)
