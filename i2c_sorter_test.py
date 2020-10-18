import sys, os,time
import smbus
import time
import redis

bus = smbus.SMBus(1)


#reg_address = [0xF4,0xF5] #Temprature
address = 0x68
Sensor_name= 'RTC'
Value = "20:10:06:05:14:00"
reg_address=[0x09,0x08,0x06,0x05,0x04,0x03]

#Estabslishing redis connection 
r= redis.Redis(host='localhost',port=6379, db=0, decode_responses=True) 
p = r.pubsub()
p.subscribe(Sensor_name)


r.publish(Sensor_name,"{TSI}:{123}")
r.publish(Sensor_name,"{GSI}:{893}")
r.publish(Sensor_name,"{ASI}:{183}")
r.publish(Sensor_name,"{TFI}:{523}")

while True:
    for key in scan_iter('{TSI}:123'):
        print(key)
    

    
    #time.sleep(3)
    
    #print(p.get_message()['data'])
    
    #time.sleep(2)





#while True:
    
# try:
#     
#      # 'YR:MO:DD:HR:MI:SS' How we want value to be inputted
#         val=Value.split(":")
#         print(val)
# 
#         bus.write_byte_data(0x68,reg_address[0],int(val[0],16)) #Year
#         bus.write_byte_data(0x68,reg_address[1],int(val[1],16))
#         bus.write_byte_data(0x68,reg_address[2],int(val[2],16))
#         bus.write_byte_data(0x68,reg_address[3],int(val[3],16))
#         bus.write_byte_data(0x68,reg_address[4],int(val[4],16))
#         bus.write_byte_data(0x68,reg_address[5],int(val[5],16))
#         
#         time.sleep(1)
# 
# except IOError:
#     time.sleep(1)

# while True:
#     try:       
#         data = ""
#         seconds_data = ""
#         mins_data = ""
#         hours_data= ""
#         days_data = ""
#         months_data = ""
#         years_data = ""
#         for i in range(len(reg_address)):
#             busval = bus.read_byte_data(address,reg_address[i])
#             if (i == 5):
#                 seconds_data = str(hex(((busval & 0xF0)>> 4))) + str(hex((busval & 0xF))) 
#             if (i == 4):
#                 mins_data = str(hex(((busval & 0xF0)>> 4))) + str(hex((busval & 0xF)))
#             if (i == 3):
#                 hours_data = str(hex(((busval & 0xF0)>> 4))) + str(hex((busval & 0xF)))
#             if (i == 2):
#                 days_data = str(hex(((busval & 0xF0)>> 4))) + str(hex((busval & 0xF))) 
#             if (i == 1):
#                 months_data = str(hex(((busval & 0xF0)>> 4))) + str(hex((busval & 0xF)))
#             if (i == 0):
#                 years_data = str(hex(((busval & 0xF0)>> 4))) + str(hex((busval & 0xF)))
#         
#         #Save to redis
#        # print((years_data + ":" + months_data + ":" + days_data + ":" + hours_data + ":" + mins_data + ":" + seconds_data).replace("0x",""))
#         time_data=  (hours_data + ":" + mins_data + ":" + seconds_data).replace("0x","")
# 
#          #Storing it into the redis database 
#         r.publish(Sensor_name,time_data)
# 
#         
#         time.sleep(1)
#         #Calling method to print out retrive data from Redis
# 
#         print(p.get_message()['data'])
# 
#              
#     except IOError:
#         time.sleep(1)




    
        


