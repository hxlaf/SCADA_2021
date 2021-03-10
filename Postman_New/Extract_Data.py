import config
import sys
import os
import psycopg2

config_path = '/usr/etc/scada/config'
sys.path.append(config_path)


class Extract_Data:


    database = psycopg2.connect(
        user='pi',
        password='scada',
        host='localhost',
        port='5432',
        database='test'
    )


    timeStampList = []
    cursor = database.cursor()


    def __init__(self):
        self.sensorList = []  # list to hold the sensors from the config file.
        print("first")
        self.getSensorList()
        print("here")
        name = self.sensorList[0]
        # self.getTimeStamps(name)
        print("HEY" + str(self.getTimeStamps(name)))


    def getTimeStamps(self, sensorName):
        """
            Return the timestamps for DRIVE mode. 
        """
        cursor.execute("""
            SELECT value, timestamp
            FROM data
            WHERE sensor_id = sensorName
            ORDER BY timestamp ASC
        """)

        data = cursor.fetchall()
        print("data " + str(data))
        if len(data) == 0:
            # If this is the case then there is an issue with the logger class' update method
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
                #print("Begin ")

            # Car just went into OFF Mode
            elif(row[0] == 'OFF' and drive_status == True):
                drive_status = False
                end_time = row[1]
                time = end_time - begin_time
                timeStampList.append(time)

        return timeStampList


    def getSensorList(self):
        self.nameList = config.get('PostProcessing')

        for name in self.nameList:
            self.sensorList.append(name)


    def getSensorData(self, sensor_id, data):
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


    def getMean(self, data):
        pass


    def getMax(self, data):
        pass


    def getMin(self, data):
        pass


    # print(self.getTimeStamps())

Data = Extract_Data()
