import sys
import os
import psycopg2


database = psycopg2.connect(
    user='pi',
    password='scada',
    host='localhost',
    port='5432',
    database='test'
)


timeStampList = []
cursor = database.cursor()

def getTimeStamps():


    """
        Return the timestamps for DRIVE mode. 
    """
    cursor.execute("""
        SELECT value, timestamp
        FROM data
        WHERE sensor_id = 'emulator_tsi_drive_state'
        ORDER BY timestamp ASC
    """)

    data = cursor.fetchall()
    if len(data)==0:
        #If this is the case then there is an issue with the logger class' update method
        return 'NO DATA FOUND FOR POSTGRES'

    # local variables for time stamps 
    drive_status = False
    begin_time = 0 
    end_time = 0

    for row in data:

        # Car just went intto DRIVE Mode
        if(row[0] == 'DRIVE' and drive_status == False):
            drive_status = True
            begin_time = row[1]

        # Car just went into OFF Mode
        elif(row[0] == 'OFF' and drive_status == True):
            drive_status = False
            end_time = row[1]
            time = end_time - begin_time
            timeStampList.append(time)

    
    
    return self.timeStampList


def getSensorData(sensor_id, data):
    pass
    # cursor.execute("""
    #     SELECT * from data
    #     WHERE sensor_id = %s
    #     ORDER BY timestamp ASC
    # """, [sensor_id])

    # data = cursor.fetchall()
    
    # if len(data)==0:
    #     #If this is the case then there is an issue with the logger class' update method
    #     return 'ERR IN DATAPATH'

    

def getMean(data):
    pass

def getMax(data):
    pass

def getMin(data):
    pass


print(getTimeStamps())