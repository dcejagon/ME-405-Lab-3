"""
    @file                    portreader_v2.py
    @brief                   serial port reader
    @description             reads lines sent from nucleo to serial port of PC. Sends input to nucleo to run code and generates plots from data collected.
    @author                  Daniel Gonzalez
    @author                  Nolan Clapp
    @author                  Caleb Kephart
    @date                    January 31, 2022
"""

import time
import serial 
from matplotlib import pyplot as plt


with serial.Serial ('COM10', 115200) as ser_port:
    
    ser_port.write (b'0\r\n')
    time.sleep(1)
    ser_port.write(b'\x03')
    data_results=[]
    while True :
        try:
            line = ser_port.readline().strip().decode()
            print (line)
            data_results.append(line)
            if line == 'Stop Data':

                raise KeyboardInterrupt    
        except KeyboardInterrupt:
            break
        

data_results = ','.join(data_results).split(',')
print(data_results)   





listOdd = data_results[1::2] # Elements from list1 starting from 1 iterating by 2
listEven = data_results[::2] # Elements from list1 starting from 0 iterating by 2

listOdd.pop(len(listOdd)-1)
listEven.pop(0)
#print (listOdd)
#print (listEven)
   
# item_x = [i.split(',', 1)[0] for i in data_results]
# print(item_x)        
   
# item_y = [i.split(',', 1)[0] for i in data_results]
# print(item_y)  
# 

plt.scatter(listOdd,listEven)
plt.plot(listOdd,listEven)


# Axis Labeling
plt.xlabel('Time (ms)') 
plt.ylabel('Encoder Position (ticks)') 
    
# Graph Title
plt.title('Lab 3 Plots') 

plt.show()

