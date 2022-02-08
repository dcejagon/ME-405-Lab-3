# -*- coding: utf-8 -*-
"""
Created on Mon Feb  7 15:08:10 2022

@author: nclap
"""

import gc
import pyb
import cotask
import task_share
import EncoderDriver
import MotorDriver
import ClosedLoop
import pyb
import time

## MOTOR PIN STUFF
en_pin=pyb.Pin (pyb.Pin.board.PA10, pyb.Pin.OUT_PP)
in1pin=pyb.Pin (pyb.Pin.board.PB4, pyb.Pin.OUT_PP)
in2pin=pyb.Pin (pyb.Pin.board.PB5, pyb.Pin.OUT_PP)
timer=3
 
en_pin2=pyb.Pin (pyb.Pin.board.PC1, pyb.Pin.OUT_PP)
in1pin2=pyb.Pin (pyb.Pin.board.PA0, pyb.Pin.OUT_PP)
in2pin2=pyb.Pin (pyb.Pin.board.PA1, pyb.Pin.OUT_PP)
timer2=5


##ENCODER PIN STUFF
ENCpin1=pyb.Pin (pyb.Pin.board.PB6)
ENCpin2=pyb.Pin (pyb.Pin.board.PB7)
timernumber=4

ENC2pin1=pyb.Pin (pyb.Pin.board.PC6)
ENC2pin2=pyb.Pin (pyb.Pin.board.PC7)
timernumber2=8

## SHARES
duty1 = task_share.Share ('f', thread_protect = False, name = "Duty_1")
duty2 = task_share.Share ('f', thread_protect = False, name = "Duty_2")
EncPosition = task_share.Share ('h', thread_protect = False, name = "Position_1")
EncPosition2 = task_share.Share ('h', thread_protect = False, name = "Position_2")
Kp1 = task_share.Share ('f', thread_protect = False, name = "Porportional_Gain")
Kp2 = task_share.Share ('f', thread_protect = False, name = "Porportional_Gain")
setpoint1 = task_share.Share ('h', thread_protect = False, name = "Set_Point1")
setpoint2 = task_share.Share ('h', thread_protect = False, name = "Set_Point2")
setpoint1.put(4096*4)
setpoint2.put(4096*4)
Kp1.put(.1)
Kp2.put(.0015)
##OBJECTS
motor1=MotorDriver.MotorDriver(en_pin, in1pin, in2pin, timer,duty1,duty2)
motor2=MotorDriver.MotorDriver(en_pin2, in1pin2, in2pin2, timer2,duty1,duty2)

ENC1=EncoderDriver.EncoderDriver(ENCpin1,ENCpin2,ENC2pin1,ENC2pin2,timernumber,timernumber2,EncPosition,EncPosition2)
ENC2=EncoderDriver.EncoderDriver(ENCpin1,ENCpin2,ENC2pin1,ENC2pin2,timernumber,timernumber2,EncPosition,EncPosition2)

Cl1=ClosedLoop.ClosedLoop(Kp1,Kp2,setpoint1,setpoint2,EncPosition,EncPosition2,duty1,duty2,time)
Cl2=ClosedLoop.ClosedLoop(Kp1,Kp2,setpoint1,setpoint2,EncPosition,EncPosition2,duty1,duty2,time)



def task1_fun ():
    '''!
        runs tasks and functions for the first motor
    '''
    while True:
    #do motor 1 stuff here
        ENC1.read()
        Cl1.control_loop()
        motor1.set_duty_cycle(duty1.get())

        yield (0)

def task2_fun ():
    '''!
        runs tasks and functions for the second motor
    '''
    while True:
        #do motor 1 stuff here
        
        ENC2.read2()
        Cl2.control_loop2()
        motor2.set_duty_cycle2(duty2.get())
        yield (0)
    
if __name__=="__main__":
    
    task1 = cotask.Task (task1_fun, name = 'Task_1', priority = 2, 
                         period = 20, profile = True, trace = False)
    task2 = cotask.Task (task2_fun, name = 'Task_2', priority = 2, 
                         period = 20, profile = True, trace = False)
    cotask.task_list.append (task1)
    cotask.task_list.append (task2)

    # Run the memory garbage collector to ensure memory is as defragmented as
    # possible before the real-time scheduler is started
    gc.collect ()

    # Run the scheduler with the chosen scheduling algorithm. Quit if any 
    # character is received through the serial port
    vcp = pyb.USB_VCP ()
    while not vcp.any ():
        cotask.task_list.pri_sched ()

    # Empty the comm port buffer of the character(s) just pressed
    vcp.read ()
    
    print ('\n' + str (cotask.task_list))
    print (task_share.show_all ())
    print (task1.get_trace ())
    print ('\r\n')

