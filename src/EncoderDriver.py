"""
    @file                    EncoderDriver.py
    @brief                   This file provides the code to interface directly with the encoder hardware
    @author                  Daniel Gonzalez
    @author                  Nolan Clapp
    @author                  Caleb Kephart
    @date                    January 24, 2022
"""

import pyb
    
class EncoderDriver:
    ''' @brief Interface with quadrature encoders
        @details This code allows us to calculate the current position in ticks of the motor shaft
    '''
        
    def __init__(self,ENCpin1,ENCpin2,ENC2pin1,ENC2pin2,timernumber,timernumber2,EncPosition1,EncPosition2):
        ''' @brief Constructs an encoder object
            @details Sets up the encoder so it is ready to run using the pins specified in some main file
            @param ENCpin1 This parameter allows us to choose which first pin our encoder will be using 
            @param ENCpin2 This parameter allows us to choose which first pin our encoder will be using
            @param timernumber This parameter chooses the correct timer number for each instance of the encoder
            
        '''
        ## @brief           Defines the first pin of the encoder
        #  @details         For example Encoder1 uses PinB6 as pin1
        self.ENCpin1=ENCpin1
        ## @brief           Defines the first pin of the encoder
        #  @details         For example Encoder2 uses PinB7 as pin2
        self.ENCpin2=ENCpin2
        ## @brief           Defines the first pin of the encoder
        #  @details         For example Encoder1 uses PinB6 as pin1
        self.ENC2pin1=ENC2pin1
        ## @brief           Defines the first pin of the encoder
        #  @details         For example Encoder2 uses PinB7 as pin2
        self.ENC2pin2=ENC2pin2
        ## @brief           Defines the timer number we will use for each encoder
        #  @details         This allows us set the timer number by passing it in to the __init__() funciton
        self.timernumber=timernumber
        ## @brief           Defines the timer number we will use for each encoder
        #  @details         This allows us set the timer number by passing it in to the __init__() funciton
        self.timernumber2=timernumber2
        ## @brief           Defines the period of the encoder 
        #  @details         Defines the period of the encoder as the largest 16 bit 
        #                   number, 65,535
        self.period=65535
        ## @brief           Keeps track of the previous count from the encoder timer
        #  @details         Defines the variable responsible for keeping track of the 
        #                   previous encoder count, used in calculating delta
        self.countprev1=0
        ## @brief           Keeps track of the previous count from the encoder timer
        #  @details         Defines the variable responsible for keeping track of the 
        #                   previous encoder count, used in calculating delta
        self.countprev2=0
        ## @brief           Defines the curent encoder position
        #  @details         This variable keeps track of the current encoder position
        self.EncPosition1 = EncPosition1
        ## @brief           Defines the curent encoder position
        #  @details         This variable keeps track of the current encoder position
        self.EncPosition2 = EncPosition2
        
        self.position1=0
        self.position2=0
        ## @brief           Sets up the on board timer on the Nucleo
        #  @details         This variable allows us to use Timer4 on the Nucleo with a period
        #                   of the largest 16 bit number with a prescaler of 0
        self.tim4 = pyb.Timer(timernumber, prescaler=0, period=65535)
        ## @brief           Sets up the on board timer on the Nucleo
        #  @details         This variable allows us to use Timer4 on the Nucleo with a period
        #                   of the largest 16 bit number with a prescaler of 0
        self.tim8= pyb.Timer(timernumber2, prescaler=0, period=65535)
        ## @brief            Defines the location of the encoder timer channel on the Nucleo
        #  @details          Defines the location of the encoder timer channel on the Nucleo
        #                    as channel 1
        self.ENCch1= self.tim4.channel(1, pyb.Timer.ENC_AB, pin=self.ENCpin1)
        ## @brief            Defines the location of the encoder timer channel on the Nucleo
        #  @details          Defines the location of the encoder timer channel on the Nucleo
        #                    as channel 2
        self.ENCch2= self.tim4.channel(2, pyb.Timer.ENC_AB, pin=self.ENCpin2)
        
        self.ENC2ch1= self.tim8.channel(1, pyb.Timer.ENC_AB, pin=self.ENC2pin1)
        ## @brief            Defines the location of the encoder timer channel on the Nucleo
        #  @details          Defines the location of the encoder timer channel on the Nucleo
        #                    as channel 2
        self.ENC2ch2= self.tim8.channel(2, pyb.Timer.ENC_AB, pin=self.ENC2pin2)
        print ('Creating a encoder driver')
        
    def read(self):
        ''' @brief Reads encoder position by calculating delta
            @details This function is responsible for reading the encoder position
            and delta values, at a constant interval defined in the main program file.
            @return position The new position of the encoder shaft
        '''
        
        ## @brief           Creates a variable that keeps track of the count
        #  @details         This variable uses the onboard coutner to determine
        #                   encoder position
        count=self.tim4.counter()
        
        ## @brief           Creates a variable that keeps track of the encoder delta
        #  @details         This variable is used to prevent counter overflow on our encoder
        delta=count-self.countprev1
        #print(delta)
 
        #check delta and fix
        if delta>= self.period/2:
            delta-=self.period
            #print(delta)
        elif delta< (-self.period/2):
        #add delta to position variable to 
            
            delta+=self.period
        #make previous count = current count
        
        self.position1+=delta
        self.EncPosition1.put(self.position1)
        
        self.countprev1=count
        
        #print(self.EncPosition1.get())
        return self.EncPosition1.get()
        
    def read2(self):
        ''' @brief Reads encoder position by calculating delta
            @details This function is responsible for reading the encoder position
            and delta values, at a constant interval defined in the main program file.
            @return position The new position of the encoder shaft
        '''
        
        ## @brief           Creates a variable that keeps track of the count
        #  @details         This variable uses the onboard coutner to determine
        #                   encoder position
        count=self.tim8.counter()
        
        ## @brief           Creates a variable that keeps track of the encoder delta
        #  @details         This variable is used to prevent counter overflow on our encoder
        delta=count-self.countprev2
        #print(delta)
 
        #check delta and fix
        if delta>= self.period/2:
            delta-=self.period
            #print(delta)
        elif delta< (-self.period/2):
        #add delta to position variable to 
            
            delta+=self.period
        #make previous count = current count
        
        self.position2+=delta
        self.EncPosition2.put(self.position2)
        
        self.countprev2=count
        
        
        return self.EncPosition2.get()
    
    def zero (self):
        ''' @brief Sets encoder position to zero
            @details sets the current encoder position to a zero value
            @return position The new position of the encoder shaft (0)
        '''
        self.EncPosition1.put(0)
        self.EncPosition2.put(0)
        #print('Zeroing Encoder')
        #print(self.EncPosition.read())
        
        return self.EncPosition1.get() and self.EncPosition2.get()


if __name__=="__main__":
    import time

    
    ENCpin1=pyb.Pin (pyb.Pin.board.PB6)
    ENCpin2=pyb.Pin (pyb.Pin.board.PB7)
    timernumber=4
    ENC1=EncoderDriver(ENCpin1,ENCpin2,timernumber)
    while True:
        try:
            
            ENC1.read()
            time.sleep(.25)
        except:
            pass
    
    