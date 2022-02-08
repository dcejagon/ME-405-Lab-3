''' @file                       MotorDriver.py
    @brief                      A driver file for interacting with motors
    @details                    This driver file interacts with motors sending duty cycle values and setting pin values to 
                                control the motor behavior.
                                
    @author                     Daniel Gonzalez
    @author                     Nolan Clapp
    @author                     Caleb Kephart
    @date                       January 24, 2022
'''
import pyb
class MotorDriver:
    ''' @brief                  This class implements a motor driver for an ME405 kit. 
        @details                Class composed of two functions to manipulate a motor.
    '''

    def __init__ (self,en_pin,in1pin,in2pin,timer):
        '''!
        Creates a motor driver by initializing GPIO
        pins and turning the motor off for safety. 
        @param en_pin (There will be several of these)
        '''
        
        ## @brief Initializes en pin
        #
        self.en_pin=en_pin
        ## @brief Initializes In1 Pin
        #
        self.in1pin=in1pin
        ## @brief Initializes In2 Pin
        #
        self.in2pin=in2pin
        ## @brief Initializes timer
        #
        self.timer=timer
        ## @brief Initializes motor timer
        #
        self.tim3 = pyb.Timer (self.timer, freq=20000)
        ## @brief Sets motor channel and pins to recieve PWM
        #
        self.ch1 = self.tim3.channel (1, pyb.Timer.PWM, pin=in1pin)
        ## @brief Sets motor channel and pins to recieve PWM
        #
        self.ch2 = self.tim3.channel (2, pyb.Timer.PWM, pin=in2pin)
        print ('Creating a motor driver')

    def set_duty_cycle (self, level):
        '''
        @brief This function allows us to set a duty cycle for the motor
        @details This method sets the duty cycle to be sent
        to the motor to the given level. Positive values
        cause torque in one direction, negative values
        in the opposite direction.
        @param level A signed integer holding the duty
               cycle of the voltage sent to the motor 
        '''
    
        self.en_pin.high()
        self.in1pin.low()
        
        if level>=0:
            self.ch1.pulse_width_percent(level)
            self.ch2.pulse_width_percent(0)
        else:
            self.ch1.pulse_width_percent(0)
            self.ch2.pulse_width_percent(abs(level))   
        print ('Setting duty cycle to ' + str (level))
        


if __name__=="__main__":
    import pyb
    en_pin=pyb.Pin (pyb.Pin.board.PA10, pyb.Pin.OUT_PP)
    in1pin=pyb.Pin (pyb.Pin.board.PB4, pyb.Pin.OUT_PP)
    in2pin=pyb.Pin (pyb.Pin.board.PB5, pyb.Pin.OUT_PP)
    timer=3
    motor1=MotorDriver(en_pin, in1pin, in2pin, timer)
    motor1.set_duty_cycle(50)
    
     