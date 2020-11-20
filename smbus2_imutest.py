import smbus
import time
# Open i2c bus 1 and read one byte from address 80, offset 0

bus = smbus.SMBus(3)
c={ "Chip Id":0x00,"Temp":0x34,"Calibration Status":0x35,"Sys Status":0x39,"ST Result":0x36,"Sys_Error":0x3a,"Unit Selection":0x3b,"Operation Mode":0x3D,
"Power Mode":0x3e,"Temp Source":0x40, "OPR Mode": 0x3D}

#Acclerometer
acc_x = [0x55,0x56]
acc_y = [0x57,0x58]
acc_z = [0x59,0x5A]

#Magnetometer 
mag_x = [0x5B,0x5C]
mag_y = [0x5D,0x5E]
mag_z = [0x5F,0x60]

#Gyro 
gyro_x = [0x61,0x62]
gyro_y = [0x63,0x64]
gyro_z = [0x65,0x66]

#Gravity 
grav_x = [0x2E,0x2F]
grav_y = [0x30,0x31]
grav_z = [0x32,0x33]

def setup():
    setCal()
    time.sleep(1)
    
    #Set the IMU to use Extenal Crystal 
    setExternalCrystal()
    
    #Operation Mode of IMU NDOF Fusion Mode 
    #bus.write_byte_data(0x28,0x3D,0x0C)
    bus.write_byte_data(0x28,0x3D,0x07)
    print ("Power Mode Setup: " + str(bus.read_byte_data(0x28,0x3D)))
    time.sleep(0.10)

    #Read a temperature this will be in deg C
    temp =bus.read_byte_data(0x28, c.get("Temp"))
    unit_selc = bus.read_byte_data(0x28, c.get("Unit Selection"))
    temp_s = bus.read_byte_data(0x28, c.get("Temp Source"))
    print( "Temperature in C: " + str(temp) + " Unit Sel: " + str(unit_selc) + " Temp Source: " + str(temp_s))


def setExternalCrystal (): 
    #Switch Configuration Mode 
     #bus.write_byte_data(0x28,0x3D,0X00)
     print ("Power Mode EC_config: " + str(bus.read_byte_data(0x28,0x3D)))
     time.sleep(0.25)
     #Set ClK_Sel to use External Oscillator of the Board 
     bus.write_byte_data(0x28,0x3F,0x80)
     time.sleep(1)
     #Setting the Mode back to NDOF Fusion
     #bus.write_byte_data(0x28,0x3D,0x0C)
     print ("Power Mode Setup EC_NDOF: " + str(bus.read_byte_data(0x28,0x3D)))
     time.sleep(1)

def setCal():
    #Setting the Calibration Units
    bus.write_byte_data(0x28,0x3B,0x82)
    time.sleep(0.25)
    #Temp Source
    bus.write_byte_data(0x28,0x40,0x01)
    time.sleep(0.25)

def readSensor(Sensor_add):
    data = 0 

    for i in range(len(Sensor_add)):
        data = data + bus.read_byte_data(0x28,Sensor_add[i]) << (8 * i)
    
    return data 
     
    
### Main 
setup()

while True:

    try:
     #Acceleration Vector
        accel_x = readSensor(acc_x)
        accel_y = readSensor(acc_y)
        accel_z = readSensor(acc_z)

        time.sleep(0.2)
        #Magnometer Vector
        magno_x = readSensor(mag_x)
        magno_y = readSensor(mag_y)
        magno_z = readSensor(mag_z)
        time.sleep(0.2)
        #Gyro
        gyrom_x = readSensor(gyro_x)
        gyrom_y = readSensor(gyro_y)
        gyrom_z = readSensor(gyro_z)
        time.sleep(0.2)
        #GRavity 
        g_x = readSensor(grav_x)
        g_y = readSensor(grav_y)
        g_z = readSensor(grav_z)
        time.sleep(0.2)

    #Printing Calibration Status 
        calibration_status = bus.read_byte_data(0x28,0x35) 
        system_cal = calibration_status >> 6 
        gyro_cali = (calibration_status >> 4) & 0x03
        acc_cali = (calibration_status >>2) & 0x03
        mag_cali = (calibration_status) & 0x03

        print("Calibration Status: " + str(calibration_status))
        print ("Power Mode: " + str(bus.read_byte_data(0x28,0x3D)))
        print( "System: " + str(system_cal) + " Gyro: "+ str(gyro_cali) + " Acc_cali: " + str(acc_cali) + "Mag_cal: " + str(mag_cali))
        print( "gyro LSB " + str(bus.read_byte_data(0x28,0x61)))
        print( "gyro MSB " + str(bus.read_byte_data(0x28,0x62)))
        print ( "gyrom_x " + str(gyrom_x))
        #print( "acc_x: "+ str(accel_x) + " acc_y: " + str(accel_y) + " acc_z: " + str(accel_z))
        #print( "magno_x: "+ str(magno_x) + " magyrogno_y: " + str(magno_y) + " magno_z: " + str(magno_z))
        #print( "gyro_x: "+ str(gyrom_x) + " gyro_y: " + str(gyrom_y) + " gyro_z: " + str(gyrom_z))
        #print( "gravity_x: "+ str(g_x) + " gravity_y: " + str(g_y) + " gravity_z: " + str(g_z))
        time.sleep(0.2)
        
    except IOError:
        print ("Im am here")
        time.sleep(.5)