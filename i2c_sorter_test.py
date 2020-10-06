import sys, os,time
import smbus
import time

bus = smbus.SMBus(1)

#reg_address = [0xF4,0xF5] #Temprature
address = 0x68
Value = "20:10:06:05:14:00"
reg_address=[0x09,0x08,0x06,0x05,0x04,0x03]
#while True:
    
try:
    
     # 'YR:MO:DD:HR:MI:SS' How we want value to be inputted
        val=Value.split(":")
        print(val)

        bus.write_byte_data(0x68,reg_address[0],int(val[0],16)) #Year
        bus.write_byte_data(0x68,reg_address[1],int(val[1],16))
        bus.write_byte_data(0x68,reg_address[2],int(val[2],16))
        bus.write_byte_data(0x68,reg_address[3],int(val[3],16))
        bus.write_byte_data(0x68,reg_address[4],int(val[4],16))
        bus.write_byte_data(0x68,reg_address[5],int(val[5],16))
        
        time.sleep(1)

except IOError:
    time.sleep(1)

while True:
    try:       
        data = ""
        seconds_data = ""
        mins_data = ""
        hours_data= ""
        days_data = ""
        months_data = ""
        years_data = ""
        for i in range(len(reg_address)):
            busval = bus.read_byte_data(address,reg_address[i])
            if (i == 5):
                seconds_data = str(hex(((busval & 0xF0)>> 4))) + str(hex((busval & 0xF))) 
            if (i == 4):
                mins_data = str(hex(((busval & 0xF0)>> 4))) + str(hex((busval & 0xF)))
            if (i == 3):
                hours_data = str(hex(((busval & 0xF0)>> 4))) + str(hex((busval & 0xF)))
            if (i == 2):
                days_data = str(hex(((busval & 0xF0)>> 4))) + str(hex((busval & 0xF))) 
            if (i == 1):
                months_data = str(hex(((busval & 0xF0)>> 4))) + str(hex((busval & 0xF)))
            if (i == 0):
                years_data = str(hex(((busval & 0xF0)>> 4))) + str(hex((busval & 0xF)))
        
        #Save to redis
        print((years_data + ":" + months_data + ":" + days_data + ":" + hours_data + ":" + mins_data + ":" + seconds_data).replace("0x",""))
        time.sleep(1)

        #reg_address = [0x03 ,0x04, 0x05]
        #address = 0x68
           # for x in range(start, stop, step)
        # data = ""
        # seconds_data = ""
        # mins_data = ""
        # hours_data= ""
        # for i in range(len(reg_address)):
        #     busval = bus.read_byte_data(address, reg_address[i])
        #     if (i == 0):
        #         seconds_data = str(hex(((busval & 0xF0)>> 4))) + str(hex((busval & 0xF))) 
        #     if (i == 1):
        #         mins_data = str(hex(((busval & 0xF0)>> 4))) + str(hex((busval & 0xF)))
        #     if (i == 2):
        #         hours_data = str(hex(((busval & 0xF0)>> 4))) + str(hex((busval & 0xF)))
        #         #print("Hours Data: " +hours_data)
                
        # print((hours_data + ":" + mins_data + ":" + seconds_data).replace("0x",""))
        #print(bus.read_byte_data(address, reg_address[2]))
        


        #for i in range(len(reg_address)):
            #data = (bus.read_byte_data(address,reg_address[i]) << (8 * i)) | data
            #print(hex(bus.read_byte_data(address,0x03)))  
        #print(data)
    except IOError:
        time.sleep(1)
    
# t = time.localtime()
# current_time = time.strftime("%H:%M:%S", t)
# print(current_time)

#DECIMAL HANDLING: Input will be broken in integer parts before and after decimal into diff reg
#Value = 1601776341
# print(hex(Value))
# print(str(hex(Value)).replace("0x",""))
# Substr(str(hex(Value)), 2, len(str(hex(Value)))))
# print(hex(Value))
# print(len(str(hex(Value))))
# print(range(len(str(hex(Value)))))
# for i in range(len(str(hex(Value)))):
#     if(i % 2 == 0):
#         print(hex(int((str(Value)[i]+str(Value)[i-1]))))

# for i in range(len(str(hex(Value)).replace("0x",""))-1):
#     if(i % 2 == 0):
#         print("i: ", i)
#         print(hex(((0xFF << i*4)&Value)>>i*4))
        #bus.write_byte(Sensor.reg_address[i/2],hex(((0xFF << i*4)&Value)>>i*4))        
        


