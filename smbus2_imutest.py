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

#Linear Acceleration
lacc_x = [0x28,0x29]
lacc_y = [0x2A,0x2B]
lacc_z = [0x2C,0x2D]

#Euler Angle
eul_x = [0x1A, 0x1B]
eul_y = [0x1C, 0x1C]
eul_z = [0x1E, 0x1F]


#Defined Constants
CONFIG_MODE= 0x00
IMU_MODE = 0x08
NDOF_MODE = 0x0C
POWER_NORMAL= 0x00
ACCEL_4G = 0x01
GYRO_2000_DPS = 0x00
MAGNETOMETER_20HZ = 0x05

#Defined Registers
OPR_MODE_REG = 0x3D
PAGE_REG = 0x07
CALIBRATION_REG = 0x35
TRIGGER_REG = 0x3F
POWER_REG = 0x3E
ACC_CONFIG_REG = 0x08
MAG_CONFIG_REG = 0x09
GYRO_CONFIG_REG = 0x0A



def reset():
    #IMU IN CONFIG MODE
    bus.write_byte_data(0x28,OPR_MODE_REG,CONFIG_MODE)
    try:
        bus.write_byte_data(0x28,TRIGGER_REG,0X20)
    except OSError:
        pass
    time.sleep(0.7)
    

def setup():
    reset()
    bus.write_byte_data(0x28,POWER_REG,POWER_NORMAL)
    bus.write_byte_data(0x28,PAGE_REG,0x00)
    bus.write_byte_data(0x28,TRIGGER_REG,0x00)
    bus.write_byte_data(0x28,ACC_CONFIG_REG,ACCEL_4G)
    bus.write_byte_data(0x28,GYRO_CONFIG_REG,GYRO_2000_DPS)
    bus.write_byte_data(0x28,MAG_CONFIG_REG,MAGNETOMETER_20HZ)
    time.sleep(0.01)
    ##Setting IMU TO NDOF MODE
    bus.write_byte_data(0x28,OPR_MODE_REG,NDOF_MODE)
    time.sleep(0.01)
    
    
#     
#     #Set the IMU to use Extenal Crystal 
#     setExternalCrystal()
#     
#     #Operation Mode of IMU NDOF Fusion Mode 
#     #bus.write_byte_data(0x28,0x3D,0x0C)
#     bus.write_byte_data(0x28,0x3D,0x07)
#     print ("Power Mode Setup: " + str(bus.read_byte_data(0x28,0x3D)))
#     time.sleep(0.8)

    #Read a temperature this will be in deg C
    temp =bus.read_byte_data(0x28, c.get("Temp"))
    #unit_selc = bus.read_byte_data(0x28, c.get("Unit Selection"))
    temp_s = bus.read_byte_data(0x28, c.get("Temp Source"))
    #print( "Temperature in C: " + str(temp) + " Unit Sel: " + str(unit_selc) + " Temp Source: " + str(temp_s))
    print( "Temperature in C: " + str(temp) + " Unit Sel: " + " Temp Source: " + str(temp_s))


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
        data = data|bus.read_byte_data(0x28,Sensor_add[i]) << (8 * i)
    
    return data 
     
    
### Main 
setup()

while True:

    try:
     #Acceleration Vector
        accel_x = readSensor(acc_x)*(1/100)
        accel_y = readSensor(acc_y)*(1/100)
        accel_z = readSensor(acc_z)*(1/100)
        
      #Linear Acceleration
        laccel_x = readSensor(lacc_x)*(1/100)
        laccel_y = readSensor(lacc_y)*(1/100)
        laccel_z = readSensor(lacc_z)*(1/100)

        time.sleep(0.2)
        #Magnometer Vector
        magno_x = readSensor(mag_x)
        magno_y = readSensor(mag_y)
        magno_z = readSensor(mag_z)
        time.sleep(0.2)
        #Gyro
        gyrom_x = readSensor(gyro_x)*0.001090830782496456
        gyrom_y = readSensor(gyro_y)*0.001090830782496456
        gyrom_z = readSensor(gyro_z)*0.001090830782496456
        time.sleep(0.2)
        #GRavity 
        g_x = readSensor(grav_x)*(1/100)
        g_y = readSensor(grav_y)*(1/100)
        g_z = readSensor(grav_z)*(1/100)
        time.sleep(0.2)
        
    #Euler Angle
        e_x = readSensor(eul_x)*(1/16)
        e_y = readSensor(eul_y)*(1/16)
        e_z = readSensor(eul_z)*(1/16)
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
#         print( "gyro LSB " + str(bus.read_byte_data(0x28,0x61)))
#         print( "gyro MSB " + str(bus.read_byte_data(0x28,0x62)))
#         print ( "gyrom_x " + str(gyrom_x))
        print( "lacc_x: "+ str(laccel_x) + " lacc_y: " + str(laccel_y) + " acc_z: " + str(laccel_z))
        #print( "acc_x: "+ str(accel_x) + " acc_y: " + str(accel_y) + " acc_z: " + str(accel_z))
        #print( "magno_x: "+ str(magno_x) + " magyrogno_y: " + str(magno_y) + " magno_z: " + str(magno_z))
#         print( "gyro_x: "+ str(gyrom_x) + " gyro_y: " + str(gyrom_y) + " gyro_z: " + str(gyrom_z))
        #print( "gravity_x: "+ str(g_x) + " gravity_y: " + str(g_y) + " gravity_z: ". + str(g_z))
       # print( "Gravity_z register val: " + str(bus.read_byte_data(0x28,0x32)) + "  2nd reg: " + str(bus.read_byte_data(0x28,0x33)))
        #print( "Binary Value of Gravity z: " + str(bin(int(g_z*100)) + " Decimal: " + str(int(g_z*100))))
        #Got the Gravity WOrking
        #if ( (g_y*100) > 1000 ):
        print( "Euler Angle_ z degrees: " + str(e_z))
        if ( (laccel_x*100) > 1000 ):
            #print("Gravity_z: " + str((-1)*(655.36-g_z)))
            print("Lin Acc_x: " + str((-1)*(655.36-laccel_x)))
            #print( "gravity_x: "+ str((-1)*(655.36-g_x)) + " gravity_y: " + str((-1)*(655.36-g_y)) + " gravity_z: " + str((-1)*(655.36-g_z)))
        else:
            #print( "gravity_x: "+ str(g_x) + " gravity_y: " + str(g_y) + " gravity_z: " + str(g_z))
            #print("Gravity_z: " + str(g_z))
            print("Linear Acceleration: " + str(laccel_x))
        time.sleep(0.2)
        
    except IOError:
        print ("Im am here")
        time.sleep(.5)