import smbus
import time
# Open i2c bus 1 and read one byte from address 80, offset 0

bus = smbus.SMBus(1)
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
    #Setting the Calibration Units 
    #bus.write_byte_data(0x28,0x3B,0x12)
    #Operation Mode of IMU NDOF Fusion Mode 
    bus.write_byte_data(0x28,0x3D,0x0C)
    #Set the IMU to use Extenal Crystal 
    setExternalCrystal() 

    #Read a temperature this will be in deg C
    temp =bus.read_byte_data(0x28, c.get("Temp"))
    print( "Temperature in C: " + str(temp) + "Unit Sel: " + str(c.get("Unit Selection")))


def setExternalCrystal (): 
    #Switch Configuration Mode 
     bus.write_byte_data(0x28,0x3D,0X00)
     time.sleep(0.25)
     #Set ClK_Sel to use External Oscillator of the Board 
     bus.write_byte_data(0x28,0x3F,0x80)
     time.sleep(0.10)
     #Setting the Mode back to NDOF Fusion
     bus.write_byte_data(0x28,0x3D,0x0C)
     time.sleep(0.20)


    


# while True:
#     for key in c :
#         try:
#             a = bus.read_byte_data(0x28, c.get(key))
#             print(key + ": " +  str(a))
#             time.sleep(1)
       
#         except IOError:
#              print("in except")
#              time.sleep(2)

    #bus.close()