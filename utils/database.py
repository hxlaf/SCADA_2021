import sys
import os
import datetime
import time
import psycopg2


database = psycopg2.connect(
    user='pi',
    password='scada',
    host='localhost',
    port='5432',
    database='test'
)

cursor = database.cursor()

def getData(sensor_id):
    """
        For a sensor name, return the value of the data associated with it,
        if it exists. To be used by other classes to retreive information
        from database.
    """
    
    cursor.execute("""
        SELECT value FROM data
        WHERE sensor_id = %s
    """, [sensor_id])
    
    data = cursor.fetchall()
    return data[0][0]