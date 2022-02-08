# Lab3 Description and Results for CoTask 

## Overall 

In this experiment we used our control system from previous exercises in a 
real-time scheduler and tested its performance by changing the timing at which 
our tasks were running. Using a motor connected to a flywheel we were able to 
test the performance of our motor system running at different motor task 
timing intervals.    

  

We encountered some issues with our control system when trying to run two 
motors simultaneously. At times our system would behave unpredictably when 
running our code or our second motor would oscillate between our desired 
setpoint, similar to having a high Kp value. 

 

## Motor Task Running Slow   

The plot below shows the system response when running the motor control task 
too slow. When the motor control task was running too slowly the controller 
could not keep up with the rest of the system and it would quickly
become unstable.  

![System Response Slow Motor Task](INSERT_IMAGE_HYPERLINK_HERE) 

## Motor Task Running Fast  

The plot below shows the system response when running the motor control 
task an adequate speed.  


![System Response Propperly Timed Motor Task](INSERT_IMAGE_HYPERLINK_HERE) 