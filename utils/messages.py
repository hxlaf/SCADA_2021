import can

FUNCTIONS = {
	# Network Management
	0x000: "NMT",

	# Sync
	0x080: "SYNC",

	# PDOs 1-4
	0x180: 'PDO-1',
	0x280: 'PDO-2',
	0x380: 'PDO-3',
	0x480: 'PDO-4',

	# SDO Write
	0x580: 'SDO-WRITE',

	# SDO Read
	0x600: 'SDO-READ',
}

def get_function(code):

	#Call to Fuction Dictionary / Hashmap that returns
	return FUNCTIONS.get(code, lambda: None)

def get_code(function):
	inv_functions = {function: code for code, function in FUNCTIONS.items()}

	return inv_functions.get(function)

def can_message(function, node_id, data):

	function_code = get_code(function)

	cob_id = function_code + node_id

	message = can.Message(arbitration_id = cob_id, data=data)
	message.is_extended_id = False

	return message

def pdo(node_id, data, pdo_number = 1):
	#http://www.byteme.org.uk/canopenparent/canopen/pdo-process-data-objects-canopen/

	data = map(lambda byte: byte % 255, data)

	return can_message('PDO-{}'.format(pdo_number), node_id, data)

def sdo_read(node_id, index, subindex=0xFF):
	#http://www.byteme.org.uk/canopenparent/canopen/sdo-service-data-objects-canopen/
	# TODO: use command byte

	command_byte = 0x00
	data = [command_byte] + index + [subindex] + [0x00, 0x00, 0x00, 0x00]

	return can_message('SDO-READ', node_id, data)

def sdo_response(node_id, index, subindex, data):
	command_byte = 0x00
	data = [command_byte] + index + [subindex] + [0x00, 0x00, 0x00, data]

	return can_message('SDO-WRITE', node_id, data)

def sdo_write(node_id, index, subindex=0xFF, value=0):
	command_byte = 0x00
	data = [command_byte] + index + [subindex] + [0x00, 0x00, 0x00, hex(value)]

	return can_message('SDO-WRITE', node_id, data)

# tkaes in can message and spits out node id and function id 
def get_info(message):
	#Attribtion ID - frame identifier used for arbitration on the bus
	cob_id = message.arbitration_id

	# get last (hex) digit of cob_id

	#Each node must have a unique id between 1 and 127
	node_id = cob_id % 16
	function_id = cob_id - node_id

	# Calling a method to determine the function
	function = get_function(function_id)

	return (function, node_id)








