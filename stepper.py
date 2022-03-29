from timeit import default_timer as timer
from time import sleep


import RPi.GPIO as GPIO

DEFAULT_SLEEP = 0.002
        

class Stepper():
    
    def __init__(self):
        
        self.STEPS = 200 # steps per revolution
        self.STEP_ANG = 1.8 # degree per step
        self.RED_FACTOR_INC = 0.2 * 0.5 # reduction factor between the motor and the backend
            # the 0.5 factor stands for the driver setting 'half-steps',
            # which reduces the vibration of the stepper.
        self.RED_FACTOR_EME = 0.2 * 0.5 # reduction factor between the motor and the backend
        self.RED_FACTOR_SAM = 0.2 * 0.5 # reduction factor between the motor and the backend
        
        self.RPM = 100.0 # revolutions per minute (should not exceed 1000 for NEMA 17 steppers)
        
        self.delay_pulseH = 0.5 / (self.RPM / 60 * self.STEPS)
        self.delay_pulseL = self.delay_pulseH
        
        # acceleration/deceleration 
        self.acc_num = 30 # number of steps of the acceleration/deceleration stage
        self.acc_init = 2 # additional factor the sleep duration
        
        self.pos_angle_incidence = 0.0
        self.pos_angle_emergence = 0.0
        self.pos_angle_sample = 0.0
        
        
        
        # definition of the PIN wiring on the Raspberry (BOARD mode)
        self.PIN_MOTORINC_ENA = 29
        self.PIN_MOTORINC_DIR = 31
        self.PIN_MOTORINC_PUL = 33
        self.PIN_MOTOREME_ENA = 40
        self.PIN_MOTOREME_DIR = 37
        self.PIN_MOTOREME_PUL = 35
        self.PIN_MOTORSAM_ENA = 32
        self.PIN_MOTORSAM_DIR = 36
        self.PIN_MOTORSAM_PUL = 38
        
        
        
        GPIO.setmode(GPIO.BOARD)
        
        GPIO.setup(self.PIN_MOTORINC_ENA, GPIO.OUT)
        GPIO.setup(self.PIN_MOTORINC_DIR, GPIO.OUT)
        GPIO.setup(self.PIN_MOTORINC_PUL, GPIO.OUT)
        GPIO.setup(self.PIN_MOTOREME_ENA, GPIO.OUT)
        GPIO.setup(self.PIN_MOTOREME_DIR, GPIO.OUT)
        GPIO.setup(self.PIN_MOTOREME_PUL, GPIO.OUT)
        GPIO.setup(self.PIN_MOTORSAM_ENA, GPIO.OUT)
        GPIO.setup(self.PIN_MOTORSAM_DIR, GPIO.OUT)
        GPIO.setup(self.PIN_MOTORSAM_PUL, GPIO.OUT)
        
        GPIO.output(self.PIN_MOTORINC_ENA, GPIO.HIGH)
        GPIO.output(self.PIN_MOTORINC_DIR, GPIO.LOW)
        GPIO.output(self.PIN_MOTORINC_PUL, GPIO.LOW)
        GPIO.output(self.PIN_MOTOREME_ENA, GPIO.HIGH)
        GPIO.output(self.PIN_MOTOREME_DIR, GPIO.LOW)
        GPIO.output(self.PIN_MOTOREME_PUL, GPIO.LOW)
        GPIO.output(self.PIN_MOTORSAM_ENA, GPIO.HIGH)
        GPIO.output(self.PIN_MOTORSAM_DIR, GPIO.LOW)
        GPIO.output(self.PIN_MOTORSAM_PUL, GPIO.LOW)
        
        
    def set_pos_angle_incidence(self, ang):
        self.pos_angle_incidence = ang
    
    def set_pos_angle_emergence(self, ang):
        self.pos_angle_emergence = ang
    
    def set_pos_angle_sample(self, ang):
        self.pos_angle_sample = ang
    
        
    def get_pos_angle_incidence(self):
        return self.pos_angle_incidence
        
    def get_pos_angle_emergence(self):
        return self.pos_angle_emergence
        
    def get_pos_angle_sample(self):
        return self.pos_angle_sample
        
        
    def woop(self, delay = DEFAULT_SLEEP, which=0):
        if(which == 0):
            GPIO.output(self.PIN_MOTORINC_PUL, GPIO.HIGH)
            sleep(delay)
            GPIO.output(self.PIN_MOTORINC_PUL, GPIO.LOW)
            sleep(delay)
        elif(which == 1):
            GPIO.output(self.PIN_MOTOREME_PUL, GPIO.HIGH)
            sleep(delay)
            GPIO.output(self.PIN_MOTOREME_PUL, GPIO.LOW)
            sleep(delay)
        elif(which == 2):
            GPIO.output(self.PIN_MOTORSAM_PUL, GPIO.HIGH)
            sleep(delay)
            GPIO.output(self.PIN_MOTORSAM_PUL, GPIO.LOW)
            sleep(delay)
        
        
        
    def move_forward(self, N, which=0):
        start = timer()
        if(which == 0):
            GPIO.output(self.PIN_MOTORINC_DIR, GPIO.LOW)
        elif(which == 1):
            GPIO.output(self.PIN_MOTOREME_DIR, GPIO.LOW)
        elif(which == 2):
            GPIO.output(self.PIN_MOTORSAM_DIR, GPIO.LOW)
        else:
            return
        if(N - 2* self.acc_num > 0):
            for i in range(self.acc_num):
                self.woop(delay = DEFAULT_SLEEP * (1 + (1 - int(i)/self.acc_num)*(self.acc_init)), which=which)
                if(which == 0):
                    self.pos_angle_incidence += self.STEP_ANG * self.RED_FACTOR_INC
                elif(which == 1):
                    self.pos_angle_emergence += self.STEP_ANG * self.RED_FACTOR_EME
                elif(which == 2):
                    self.pos_angle_sample += self.STEP_ANG * self.RED_FACTOR_SAM
                
            for i in range(N - 2*self.acc_num):
                self.woop(which=which)
                if(which == 0):
                    self.pos_angle_incidence += self.STEP_ANG * self.RED_FACTOR_INC
                elif(which == 1):
                    self.pos_angle_emergence += self.STEP_ANG * self.RED_FACTOR_EME
                elif(which == 2):
                    self.pos_angle_sample += self.STEP_ANG * self.RED_FACTOR_SAM
                
            for i in range(self.acc_num):
                self.woop(delay = DEFAULT_SLEEP * (1 + (int(i)/self.acc_num)*(self.acc_init)), which=which)
                if(which == 0):
                    self.pos_angle_incidence += self.STEP_ANG * self.RED_FACTOR_INC
                elif(which == 1):
                    self.pos_angle_emergence += self.STEP_ANG * self.RED_FACTOR_EME
                elif(which == 2):
                    self.pos_angle_sample += self.STEP_ANG * self.RED_FACTOR_SAM
                
        else:
            for i in range(N//2):
                self.woop(delay = DEFAULT_SLEEP * (1 + (1 - int(i)/self.acc_num)*(self.acc_init)), which=which)
                if(which == 0):
                    self.pos_angle_incidence += self.STEP_ANG * self.RED_FACTOR_INC
                elif(which == 1):
                    self.pos_angle_emergence += self.STEP_ANG * self.RED_FACTOR_EME
                elif(which == 2):
                    self.pos_angle_sample += self.STEP_ANG * self.RED_FACTOR_SAM
                
            for i in range(N - N//2):
                self.woop(delay = DEFAULT_SLEEP * (1 + ((self.acc_num -(N - N//2) + int(i)+1)/self.acc_num)*(self.acc_init)), which=which)
                if(which == 0):
                    self.pos_angle_incidence += self.STEP_ANG * self.RED_FACTOR_INC
                elif(which == 1):
                    self.pos_angle_emergence += self.STEP_ANG * self.RED_FACTOR_EME
                elif(which == 2):
                    self.pos_angle_sample += self.STEP_ANG * self.RED_FACTOR_SAM
                
                
        end = timer()
        if(which == 0):
            print("move forward took {0:.5f} sec, incidence position is {1:.2f} deg.".format(end-start, self.pos_angle_incidence))
        elif(which == 1):
            print("move forward took {0:.5f} sec, emergence position is {1:.2f} deg.".format(end-start, self.pos_angle_emergence))
        elif(which == 2):
            print("move forward took {0:.5f} sec, sample position is {1:.2f} deg.".format(end-start, self.pos_angle_sample))
        

    def move_backward(self, N, which=0):
        start = timer()
        if(which == 0):
            GPIO.output(self.PIN_MOTORINC_DIR, GPIO.HIGH)
        elif(which == 1):
            GPIO.output(self.PIN_MOTOREME_DIR, GPIO.HIGH)
        elif(which == 2):
            GPIO.output(self.PIN_MOTORSAM_DIR, GPIO.HIGH)
        else:
            return
        
        if(N - 2* self.acc_num > 0):
            for i in range(self.acc_num):
                self.woop(delay = DEFAULT_SLEEP * (1 + (1 - int(i)/self.acc_num)*(self.acc_init)), which=which)
                if(which == 0):
                    self.pos_angle_incidence -= self.STEP_ANG * self.RED_FACTOR_INC
                elif(which == 1):
                    self.pos_angle_emergence -= self.STEP_ANG * self.RED_FACTOR_EME
                elif(which == 2):
                    self.pos_angle_sample -= self.STEP_ANG * self.RED_FACTOR_SAM
                
            for i in range(N - 2*self.acc_num):
                self.woop(which=which)
                if(which == 0):
                    self.pos_angle_incidence -= self.STEP_ANG * self.RED_FACTOR_INC
                elif(which == 1):
                    self.pos_angle_emergence -= self.STEP_ANG * self.RED_FACTOR_EME
                elif(which == 2):
                    self.pos_angle_sample -= self.STEP_ANG * self.RED_FACTOR_SAM
                
            for i in range(self.acc_num):
                self.woop(delay = DEFAULT_SLEEP * (1 + (int(i)/self.acc_num)*(self.acc_init)), which=which)
                if(which == 0):
                    self.pos_angle_incidence -= self.STEP_ANG * self.RED_FACTOR_INC
                elif(which == 1):
                    self.pos_angle_emergence -= self.STEP_ANG * self.RED_FACTOR_EME
                elif(which == 2):
                    self.pos_angle_sample -= self.STEP_ANG * self.RED_FACTOR_SAM
                
        else:
            for i in range(N//2):
                self.woop(delay = DEFAULT_SLEEP * (1 + (1 - int(i)/self.acc_num)*(self.acc_init)), which=which)
                if(which == 0):
                    self.pos_angle_incidence -= self.STEP_ANG * self.RED_FACTOR_INC
                elif(which == 1):
                    self.pos_angle_emergence -= self.STEP_ANG * self.RED_FACTOR_EME
                elif(which == 2):
                    self.pos_angle_sample -= self.STEP_ANG * self.RED_FACTOR_SAM
                
            for i in range(N - N//2):
                self.woop(delay = DEFAULT_SLEEP * (1 + ((self.acc_num -(N - N//2) + int(i)+1)/self.acc_num)*(self.acc_init)), which=which)
                if(which == 0):
                    self.pos_angle_incidence -= self.STEP_ANG * self.RED_FACTOR_INC
                elif(which == 1):
                    self.pos_angle_emergence -= self.STEP_ANG * self.RED_FACTOR_EME
                elif(which == 2):
                    self.pos_angle_sample -= self.STEP_ANG * self.RED_FACTOR_SAM
                
                
        end = timer()
        if(which == 0):
            print("move backward took {0:.5f} sec, incidence position is {1:.2f} deg.".format(end-start, self.pos_angle_incidence))
        elif(which == 1):
            print("move backward took {0:.5f} sec, emergence position is {1:.2f} deg.".format(end-start, self.pos_angle_emergence))
        elif(which == 2):
            print("move backward took {0:.5f} sec, sample position is {1:.2f} deg.".format(end-start, self.pos_angle_sample))
        

    def goto_inc(self, ang):
        move_ang = ang - self.pos_angle_incidence
        move_N = int(abs(move_ang) / (self.STEP_ANG * self.RED_FACTOR_INC))
        
        if move_ang > 0:
            expected_pos = self.pos_angle_incidence + move_N * (self.STEP_ANG * self.RED_FACTOR_INC)
            exceeded_pos = self.pos_angle_incidence + (move_N + 1) * (self.STEP_ANG * self.RED_FACTOR_INC)
            if(abs(expected_pos - ang) > abs(exceeded_pos - ang)):
                self.move_forward(move_N + 1, which=0)
            else:
                self.move_forward(move_N, which=0)
        else:
            expected_pos = self.pos_angle_incidence - move_N * (self.STEP_ANG * self.RED_FACTOR_INC)
            exceeded_pos = self.pos_angle_incidence - (move_N + 1) * (self.STEP_ANG * self.RED_FACTOR_INC)
            if(abs(expected_pos - ang) > abs(exceeded_pos - ang)):
                self.move_backward(move_N + 1, which=0)
            else:
                self.move_backward(move_N, which=0)
                
    def goto_eme(self, ang):
        move_ang = ang - self.pos_angle_emergence
        move_N = int(abs(move_ang) / (self.STEP_ANG * self.RED_FACTOR_EME))
        
        if move_ang > 0:
            expected_pos = self.pos_angle_emergence + move_N * (self.STEP_ANG * self.RED_FACTOR_EME)
            exceeded_pos = self.pos_angle_emergence + (move_N + 1) * (self.STEP_ANG * self.RED_FACTOR_EME)
            if(abs(expected_pos - ang) > abs(exceeded_pos - ang)):
                self.move_forward(move_N + 1, which=1)
            else:
                self.move_forward(move_N, which=1)
        else:
            expected_pos = self.pos_angle_emergence - move_N * (self.STEP_ANG * self.RED_FACTOR_EME)
            exceeded_pos = self.pos_angle_emergence - (move_N + 1) * (self.STEP_ANG * self.RED_FACTOR_EME)
            if(abs(expected_pos - ang) > abs(exceeded_pos - ang)):
                self.move_backward(move_N + 1, which=1)
            else:
                self.move_backward(move_N, which=1)
                
    def goto_sam(self, ang):
        move_ang = ang - self.pos_angle_sample
        move_N = int(abs(move_ang) / (self.STEP_ANG * self.RED_FACTOR_SAM))
        
        if move_ang > 0:
            expected_pos = self.pos_angle_sample + move_N * (self.STEP_ANG * self.RED_FACTOR_SAM)
            exceeded_pos = self.pos_angle_sample + (move_N + 1) * (self.STEP_ANG * self.RED_FACTOR_SAM)
            if(abs(expected_pos - ang) > abs(exceeded_pos - ang)):
                self.move_forward(move_N + 1, which=2)
            else:
                self.move_forward(move_N, which=2)
        else:
            expected_pos = self.pos_angle_sample - move_N * (self.STEP_ANG * self.RED_FACTOR_SAM)
            exceeded_pos = self.pos_angle_sample - (move_N + 1) * (self.STEP_ANG * self.RED_FACTOR_SAM)
            if(abs(expected_pos - ang) > abs(exceeded_pos - ang)):
                self.move_backward(move_N + 1, which=2)
            else:
                self.move_backward(move_N, which=2)
                
    
    def cleanup(self):
        GPIO.cleanup()
                
                
                
if __name__ == "__main__":          
    stepper = Stepper()

    stepper.set_pos_angle_incidence(0.0)
    stepper.set_pos_angle_emergence(0.0)
    stepper.set_pos_angle_sample(0.0)

    stepper.goto_inc(30.0)
    sleep(0.2)
    stepper.goto_inc(-30.0)
    sleep(0.2)
    stepper.goto_inc(0.0)
    sleep(0.2)
    
    stepper.goto_eme(30.0)
    sleep(0.2)
    stepper.goto_eme(-30.0)
    sleep(0.2)
    stepper.goto_eme(0.0)
    sleep(0.2)
    
    stepper.goto_sam(30.0)
    sleep(0.2)
    stepper.goto_sam(-30.0)
    sleep(0.2)
    stepper.goto_sam(0.0)
    sleep(0.2)
    
#    import numpy

#     i = 0
#     for a in numpy.random.uniform(low=-60, high=60, size=10):
#         print("MC {0}:: goto({1:.2f})".format(i, a))
#         stepper.goto(a)
#         sleep(0.2)
#         i += 1
    
    stepper.cleanup()
