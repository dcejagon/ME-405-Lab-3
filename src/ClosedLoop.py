"""
    @file                    ClosedLoop.py
    @brief                   This file provides the code to interface directly with the encoder hardware
    @author                  Daniel Gonzalez
    @author                  Nolan Clapp
    @author                  Caleb Kephart
    @date                    January 31, 2022
"""
import utime
import time
#from matplotlib import pyplot as plt

class ClosedLoop:
    ''' @brief Puts system into a closed loop.
        @details This code allows us to run the motor/encoder system within a closed loop.
    '''
    
    def __init__(self,Kp1,Kp2,setpoint1,setpoint2,EncPosition1,EncPosition2,duty1, duty2,time):
        ''' @brief          Constructs a closed loop object
            @details        Sets up the closed loop so that it can intake data from the encoder and main to send to the motor driver.
            @param Kp       This parameter allows us to choose the gain utilized by the system
            @param EncPosition  This parameter allows for the class to intake the encoder position data
            @param duty     This parameter chooses the duty cycle for the motor
            @param time     This parameter sets a timer to be used for the data collection
            
        '''
        ## @brief System Gain for motor 1
        #
        self.Kp1=Kp1 
        ## @brief System Gain for motor 2
        #
        self.Kp2=Kp2
        ## @brief Desired encoder position
        #
        self.setpoint1=setpoint1
        ## @brief Desired encoder position
        #
        self.setpoint2=setpoint2
        ## @brief Actual Encoder Position
        #  @details Allows for the class to read encoder position data from the 
        #           encoder.
        #
        self.EncPosition1=EncPosition1
        ## @brief Actual Encoder Position
        #  @details Allows for the class to read encoder position data from the 
        #           encoder.
        #
        self.EncPosition2=EncPosition2
        ## @brief sets duty cycle for motor
        #
        self.duty1=duty1
        ## @brief sets duty cycle for motor
        #
        self.duty2=duty2
        
        ## @brief sets timer for data collection
        #
        self.time=time
        ## @brief array of time data
        #
        self.Time1=[]
        ## @brief array of actual position data
        #
        self.Pos1=[]
        ## @brief starting time of data collection 
        #
        ## @brief array of time data
        #
        self.Time2=[]
        ## @brief array of actual position data
        #
        self.Pos2=[]
        ## @brief starting time of data collection 
        #
        self.starttime=time.ticks_ms()
    def Setpoint(self,setpoint1,setpoint2):
        '''!
            Accesses the setpoint shares to set final encoder position for each motor.
        '''
        self.setpoint1=setpoint1.get()
        self.setpoint2=setpoint2.get()
        
    def SetKp(self,Kp):
        '''!
            accesses Kp share 
        '''
        self.Kp=Kp.get()
        
            
    def control_loop(self):
        '''!
            funciton will put motor in a closed loop with the desired setpoint and gain.
        '''
        #Motor1
        
        ## @brief the error between actual and desired position
        #
        self.error1=self.EncPosition1.get()-self.setpoint1.get()
        ## @brief the duty cycle required for the system to correct with set gain.
        # 
        self.actuation1=self.Kp1.get()*self.error1
        
        self.duty1.put(self.actuation1)
        
        
        utime.sleep_ms(10)
        #print(time.ticks_ms(),self.EncPosition.get())
        
        self.Time1.append(time.ticks_diff(time.ticks_ms(),self.starttime))
        self.Pos1.append(self.EncPosition1.get())
    def control_loop2(self):
        '''!
            same function as previous but for second motor
        '''
        # Motor 2
        self.error2=self.EncPosition2.get()-self.setpoint2.get()
        ## @brief the duty cycle required for the system to correct with set gain.
        # 
        self.actuation2=self.Kp2.get()*self.error2
        print(self.actuation2)
        self.duty2.put(self.actuation2)
        #print(self.EncPosition2.get())
        
        utime.sleep_ms(10)
        #print(time.ticks_ms(),self.EncPosition.get())
        
        self.Time2.append(time.ticks_diff(time.ticks_ms(),self.starttime))
        self.Pos2.append(self.EncPosition2.get())
        #print(self.EncPosition1.get(), ',',self.EncoderPosition2.get())

    def printdata(self):
        '''!
            displays lists for time and encoder position while the task runs
        '''
        ## @brief index of arrays
        #
        n=0
        while n< len(self.Time1):
            print(self.Time1[n],',',self.Pos1[n])
            n=n+1
        

    
        
        
    
    
    
        

