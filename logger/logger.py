# THIS IS THE ONE I COMMENTED -Harry

#!/usr/bin/python3

import datetime
import time
import psycopg2
import redis
import config
import sys
import os

lib_path = '/usr/etc/scada'
config_path = '/usr/etc/scada/config'

sys.path.append(lib_path)
sys.path.append(config_path)

# Harry: import dependent python libraries

# Harry: creates instance of Redis
car_state = redis.Redis(host='localhost', port=6379,
                        db=0, decode_responses=True)
# Harry: connection object that connects to Postrges database
database = psycopg2.connect(
	user='fsae',
	password='cables',
	host='localhost',
	port='5432',
	database='demo'
)

# Harry: creates Publish/Subscribe Redis object called 'p'
p = car_state.pubsub()
# Harry: p subscribes to get messages from 3 channels in Redis
p.subscribe('bus_data')
p.subscribe('calculated_data')
p.subscribe('new-session')

# Harry: create Postrgres database cursor
# Harry: a cursor is like a dummy user in a database that executes commands and retrieves results
cursor = database.cursor()

# Uncomment this to wipe the database on startup of
# this script, sometimes useful when debugging
#
# cursor.execute("""
# 	DROP TABLE IF EXISTS sensors;
# 	DROP TABLE IF EXISTS data;
# """)

# Make sure both of our tables exist before starting
cursor.execute("""
CREATE TABLE IF NOT EXISTS data(
	id SERIAL PRIMARY KEY,
	sensor_id VARCHAR(255) NOT NULL,
	value VARCHAR(255),
	timestamp TIMESTAMP DEFAULT NOW()
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS sensors(
	id SERIAL PRIMARY KEY,
	redis_key VARCHAR(255) NOT NULL UNIQUE,
	display_name VARCHAR(255),
	datatype VARCHAR(255),
	unit VARCHAR(255)
);
""")

# Harry: commits transactions above to the database
database.commit()


# Harry: FOR SOME REASON METHOD DEFINITIONS ARE IN THE MIDDLE OF THIS FILE

def delimit_session():
	"""
		Insert a session delimiter into the data table.
		This is a row with sensor_id of "scada:session"
		and value of "NEW-SESSION"
	"""
	# Harry: This is the statement that has tabulation errors
	# Harry: THE REASON IS RANDOM SPACES AND INDENTS AFTER THE "INSERT INTO" LINE
	cursor.execute("""
		INSERT INTO data (sensor_id, value)
		VALUES ('scada:session', 'NEW-SESSION');
	""")

# Harry: WHY IS THIS CODE IN THE MIDDLE OF THE METHOD DEFINITIONS?
# Harry: initializes dictionary that will hold all the previous values from any "key"
# Harry: I'm pretty sure a key is a sensor/sensor data point
previous_values = {}

def check_update_ready(key):
	"""
		For a given key, determine if a new row should be added
		to the data table or not. It does this by checking the
		key against a locally stored dictionary of recently logged
		keys, called previous_values. The dictionary stores both the
		last value logged and the time it was logged. The function
		will return true if either the values are different, or if
		it has been more than a minute since the key was logged last.
	"""

	value, timestamp = previous_values.get(key, (None, datetime.datetime.now()))

	# Always update if the current and previous values are different
	if value != car_state.get(key):
		return True

	# If they are the same, only update if a set amount of time has elapsed
	elapsed_time = datetime.datetime.now() - timestamp
	if elapsed_time > datetime.timedelta(seconds=60):
		return True

	# default
	return False

def update(message, key):
	# Don't log the value if an identical
	# value has been logged recently

	if not check_update_ready(key):
		return

	# Harry: Builds list of all the ignore keys (why is it doing this every time it updates??)
	ignore_keys = []
	for key_string in config.get('dont_log', []):
		ignore_keys = ignore_keys + car_state.keys(key_string)
	
	if not key in ignore_keys:
		# Harry: attempts to put sensor key in the sensor table if not already
		# Harry: WHY IS THIS DONE ON EVERY UPDATE? This should be in the config.py, right?
		# Harry: Unless the idea here is to only have sensor info for the sensors involved in any
		# 		 data session. Seems inefficient though.
		cursor.execute("""
			INSERT INTO sensors
			(redis_key)
			VALUES (%s)
			ON CONFLICT (redis_key) DO NOTHING
		""", [key])
		
		#Harry: adds data to data table
		cursor.execute("""
			INSERT INTO data (sensor_id, value)
			VALUES (%s, %s)
		""", [key, car_state.get(key)])

		# Harry: updates previous value/timestamp for check_update_ready method on next loop
		previous_values[key] = (car_state.get(key), datetime.datetime.now())

		# Hary: I think this method should call "database.commit()" here

# Harry: THIS IS THE ACTUAL CODE THAT RUNS

while True:
	# Harry: Redis object gets the next message from its subscribed channels if one is available
	# Harry: Note: this "message" object is just a dict with keys 'type', 'pattern', 'channel', and 'data'
	message = p.get_message()
	if message:
		# Harry: calls update method (checks if it should be logged and executes database queries to log it)
		if message['channel'] in ['bus_data', 'calculated_data']:  
			update(message['channel'], message['data'])
			#Harry: to get live view, we could print the "previous_values" table here
		elif message['channel'] == 'new-session':
			delimit_session()		 

	# Harry: if no messages available, commit changes to database and wait for next loop
	else:
		database.commit()
		time.sleep(0.1)
