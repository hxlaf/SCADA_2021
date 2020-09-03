class Sensor:
    # variables
    
    #value
    #units
    #calibration
    #subsystem
    #lastMessageTime

    def __init__(self, name, units, dataType, subSystem):
        self.name = name
        self.units = units
        self.dataType = dataType
        self.subSystem = subSystem

    def __init__(self, configRow):
        self.name = configRow[0]
        self.units = configRow[1]
        self.dataType = configRow[2]
        self.subSystem = configRow[3]

    # methods
    def receiveMessage(self, msg):
        #gets message
        #call calibrator to calibrate value
        #stores calibrated value to value


    def getValue(self):
        #does nothing yet


class Message:
    #variables

    #sensor
    #value
    #time

    #CAN components?




