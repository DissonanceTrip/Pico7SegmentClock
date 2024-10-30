#import stuff we need. Don't change this
from machine import Pin, PWM 
from time import sleep 
import time 
import machine 
import math

#Dont change this
#Define the Servo Class for controlling servos. Credit to redoxcode: https://github.com/redoxcode/micropython-servo
class Servo:
    def __init__(self,pin_id,min_us=544.0,max_us=2400.0,min_deg=0.0,max_deg=180.0,freq=50):
        self.pwm = machine.PWM(machine.Pin(pin_id))
        self.pwm.freq(freq)
        self.current_us = 0.0
        self._slope = (min_us-max_us)/(math.radians(min_deg)-math.radians(max_deg))
        self._offset = min_us
        
    def write(self,deg):
        self.write_rad(math.radians(deg))

    def read(self):
        return math.degrees(self.read_rad())
        
    def write_rad(self,rad):
        self.write_us(rad*self._slope+self._offset)
    
    def read_rad(self):
        return (self.current_us-self._offset)/self._slope
        
    def write_us(self,us):
        self.current_us=us
        self.pwm.duty_ns(int(self.current_us*1000.0))
    
    def read_us(self):
        return self.current_us

    def off(self):
        self.pwm.duty_ns(0)

###
###
###This section has variables for you to change

#Change this pin value to match the pin you have plugged the servo into:
testservo = Servo(pin_id=0)

#This is the value we are testing. Change this around and see what works best!
degrees = 20

###
###
### END Variable section

### 
###
###These are the tests. Do not change these

#This will set the servo to the 0 position
def runTestSetZero():
    testservo.write(0)
    
#This will make the clock count up one number at a time with a 2 second pause after each number. 
def runTestCount():
    i = 0
    while i <= 9:
        testservo.write(i * degrees)
        i += 1
        time.sleep(2)

#This test will make the display/servo count up from 0 to 9 like normal then go from 9 to 0 in one fast motion.
#This happens often, so it is a good thing to check. 
def runTestFullRange():
    i = 0
    while i <= 9:
        testservo.write(i * degrees)
        i += 1
        time.sleep(1)
    time.sleep(2)
    testservo.write(0)
    
###
###
### END test section

### MAIN SECTION
###
###
#This is where stuff actually happens. Follow these steps
# First, plug one servo into the pin you specified above.
# Second, run the code, as is, to set the servo to the 0 position.
# Third, set your display to 0 then attach the servo with the gears and everything.
# Fourth, comment out the "runTestSetZero()" line below by adding a '#' to the start of it
# Fifth, uncomment the "runTestCount()" line below by removing the '#' at the start of it. Run the code and see if it counts properly.
# Sixth, adjust the degree angle as needed. If the clock overshoots, lower the value, if it undershoots, raise the value.
# Finally, repeat this process for each servo/display! You should be good to go!
# Bonus: You can comment out the first two tests below ("testservo.write(0)" and "runTestCount()") then do runTestFullRange() to stress test everything

# Test 1: set servo to 0 position
runTestSetZero()

# Test 2: make servo count up from 0 to 9 with 2 second pause between each number
#runTestCount()

# comment out the two tests above before you run this.
# Test 3: Full range test
# This test is used to make sure everything works properly when the servo moves through the full range 9 to 0
# this movement happens often, and sometimes gears can slip or the servo gets messed up somehow.
# this test is primarily to see that your build is stable enough to not get messed up when moving from 9 to 0

#runTestFullRange()
