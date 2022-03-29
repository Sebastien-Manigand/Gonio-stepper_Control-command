# -*- coding: utf-8 -*-
"""
Created on Tue Mar 30 08:31:17 2021

@author: sebas
"""


import serial
import time



try:
    serial_steppers = serial.Serial(
            'COM22',
            baudrate = 9600,
            timeout  = 0.25,
            bytesize = serial.EIGHTBITS,
            parity   = serial.PARITY_NONE,
            stopbits = serial.STOPBITS_ONE,
        )
except:
    print("ERROR: Failed to open the communication through \'COM22\'")
    exit()


running = True

while(running):
    cmd = input('command?>> ')
    
    if(cmd == 'q' or cmd == 'quit' or cmd == 'exit'):
        serial_steppers.write('exit\n'.encode('utf-8'))
        running = False
    else:
        try:
            serial_steppers.write(('%s\n'%cmd).encode('utf-8'))
            print("cmd: '{0}' successfully sent!".format(cmd))
        except:
            print("Failed to send the cmd, the communication might be broken.")
            #running = False
        
            
serial_steppers.close()


        
    
