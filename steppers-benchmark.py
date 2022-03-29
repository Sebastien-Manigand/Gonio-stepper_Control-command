
#exec(open('stepper.py').read())
from stepper import Stepper
import serial
import time


stepper = Stepper()

serial_master = serial.Serial('/dev/ttyS0',
                baudrate = 9600,
                parity = serial.PARITY_NONE,
                stopbits = serial.STOPBITS_ONE,
                bytesize = serial.EIGHTBITS,
                timeout = 0.25)

running = True

while(running):
    #cmd = input(">> ")
    cmd = serial_master.read_until('\n').decode('utf-8')
    
    if(cmd != ''):
        '''reading = True
        while(reading):
            char = serial_master.read()
            if(char != '\n'):
                cmd = cmd + char
                time.sleep(0.01)
            else:
                reading = False'''
        
        if(cmd[0:9] == 'goto_inc('):
            try:
                angle = float(cmd[9:].split(')')[0])
                print('cmd goto({0})'.format(angle))
                stepper.goto_inc(angle)
            except:
                print("Syntax error: goto(float angle)")
                
        elif(cmd[0:7] == 'get_inc'):
            print("current incidence: {0:.2f} deg".format(stepper.get_pos_angle_incidence()))
            
                
        elif(cmd[0:9] == 'goto_eme('):
            try:
                angle = float(cmd[9:].split(')')[0])
                print('cmd goto({0})'.format(angle))
                stepper.goto_eme(angle)
            except:
                print("Syntax error: goto(float angle)")
                
        elif(cmd[0:7] == 'get_eme'):
            print("current emergence: {0:.2f} deg".format(stepper.get_pos_angle_emergence()))
            
                
        elif(cmd[0:9] == 'goto_sam('):
            try:
                angle = float(cmd[9:].split(')')[0])
                print('cmd goto({0})'.format(angle))
                stepper.goto_sam(angle)
            except:
                print("Syntax error: goto(float angle)")
                
        elif(cmd[0:7] == 'get_sam'):
            print("current sample: {0:.2f} deg".format(stepper.get_pos_angle_sample()))
            
                
        elif(cmd[0] == 'q' or cmd[0:4] == 'quit' or cmd[0:4] == 'exit'):
            running = False
        
        else:
            print("Syntax error: I do not speak this language, no one does...")
            
    else:
        time.sleep(0.1)
        
#except KeyboardInterrupt:
    # here is the code you run before it exits when you press CTRL+C
    #print("Keyboard interrupt")
    
#except:
#   print("other error or exception occurred")
    
#finally:
stepper.cleanup()
serial_master.close()
