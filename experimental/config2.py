import csv
from experimental import Sensor

# with open('SensorConfig.csv') as csvfile:
#     reader = csv.reader(csvfile)
#     for row in reader:
#         print (', '.join(row))


with open('SensorConfig.csv') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        for item in row:
            print(item)
        #create Sensor object

# inserting line to test git update, adding this edit to test again and again and again