#import some modules we need to do all the cool stuff 
from machine import Pin, PWM #for servo control
from time import sleep #for sleepin'
import network #for wifi
import time #I know that I imported sleep from time above, don't judge me
import ntptime #for syncing time from public NTP server
import socket #not currently used as far as I remember, but leaving it in anyway
import machine #yeah I did it again - whatever
import math #for doing some math stuff
import requests #for the web requests for APIs for getting UTC offset and whatnot
import json #for processing results from the APIs
from secrets import ssid, password #for your wifi name and password
# ^^^^^ For the secrets.py file you need to update it with your WiFi ssid and password.

#Define the Servo Class for controlling servos. Credit to redoxcode: https://github.com/redoxcode/micropython-servo
#Loading the module itself did not work for me, so I just copied the class directly.
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
### define a few things that are used elsewhere. Make changes to stuff here as needed!
###
###
###
#define wlan for the pico W - used in wlan_connect and wlan_disconnect. Do not change this unless you know what you're doing.
wlan = network.WLAN(network.STA_IF)

#define the UTC_OFFSET which will be set again later and used to ensure correct time is displayed.
#you can statically set this and remove the methods that would change it, if you prefer. Example (PDT): -7 * 60 * 60
UTC_OFFSET = 0

#Set Servo Pins and Name them for their position - CHANGE THIS FOR YOUR PINS !!!!
hoursTens = Servo(pin_id=0)
hoursOnes = Servo(pin_id=4)
minutesTens = Servo(pin_id=8)
minutesOnes = Servo(pin_id=12)

#this variable is used to define how much angle should be used to rotate the display to the next number. 20 = 20 degrees and works for me.
#for some brands of PLA/PETG I found that 19 was better, but 20 seemed to work perfectly for my final version.
#use the "degreetest.py" file to figure out which value works best for your displays and use that value here.
degrees = 20

#define how to connect to the wifi using secrests file info - credit to example code: https://projects.raspberrypi.org/en/projects/get-started-pico-w/2
def wlan_connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    #wait for connect or fail
    max_wait = 10
    while max_wait > 0:
        if wlan.status() < 0 or wlan.status() >=3:
            break
        max_wait -= 1
        print("Waiting for connection...")
        time.sleep(1)
    #handle connection error
    if wlan.status() != 3:
        print("Network Connection Failed - restarting")
        machine.reset()
    else:
        print('Connected:')
        status = wlan.ifconfig()
        print('ip = ' + status[0])
        ip = status[0]
        return ip
    
#define how to disconnect from wifi to save power and not stress the system
def wlan_disconnect():
    print("disconnecting wifi")
    wlan.disconnect()
    time.sleep(1)
    while wlan.active():
        print("disconnecting wifi - again")
        wlan.disconnect()
        time.sleep(1)
    print("wireless disconnected")
    wlan.deinit()
    time.sleep(1)
    print("deinit wlan for full off")
    while wlan.status() != 0:
        print("deinit wlan again")
        wlan.deinit()
        time.sleep(1)
    print("wlan status is 0. Should be fully shut down")
    
# Set all servos to the 0 position.
def setALLZERO():
    hoursTens.write(0)
    time.sleep(0.5)
    hoursOnes.write(0)
    time.sleep(0.5)
    minutesTens.write(0)
    time.sleep(0.5)
    minutesOnes.write(0)

#set servos to display 1337 cause we are 1337 H@x0r2 :P
#This is to indicate successful network connection - this could be anything you want, but I did 1337 because I am a loser.
#If you want to change this to something other than 1337, just change the numbers before the "* degrees" part of each line.
def setWlanSuccess():
    hoursTens.write(1 * degrees)
    time.sleep(0.5)
    hoursOnes.write(3 * degrees)
    time.sleep(0.5)
    minutesTens.write(3 * degrees)
    time.sleep(0.5)
    minutesOnes.write(7 * degrees)
    
#Function to update time via network - get utc offset easy way and sync from ntp server
def get_time_AIO():
    global UTC_OFFSET
    print("running primary time sync")
    response = requests.get("http://worldtimeapi.org/api/ip", timeout=5)
    # Get response code
    #response_code = response.status_code
    # Get response content
    response_content = response.content
    #load data json format
    data = json.loads(response_content)
    #extract the utc_offset value
    currentoffset=data["utc_offset"]
    print("offset: ",currentoffset)
    currentoffset = currentoffset.replace(":","").replace("0","")
    print("formatted offset: ",currentoffset)
    UTC_OFFSET = int(currentoffset) * 60 * 60
    #sync time to ntp server
    ntptime.settime()
    print("time is synced and offset is set")
    response.close()
    
#backup time function that does more stuff to get the same result
def get_time_backup():
    global UTC_OFFSET
    print("Running backup time sync")
    response = requests.get("https://api.ipify.org").text
    currentip=response
    print("Public IP: ",currentip)
    url = "https://timeapi.io/api/timezone/ip?ipAddress={}".format(currentip)
    response = requests.get(url)
    #response_code = response.status_code
    # Get response content
    response_content = response.content
    data = json.loads(response_content)
    currentoffset=data["currentUtcOffset"]
    print("Current UTC Offset Seconds: ",currentoffset["seconds"])
    UTC_OFFSET = int(currentoffset["seconds"])
    ntptime.settime()
    print("time is synced and offset is set")
    response.close()

#Function to update time via network and reset if it fails more than 3 times. Not currently used due to power consumption concerns.
def updateTimeNoFail():
    error = 0
    if error < 3:
        try:
            ntptime.settime()
            print("Time updated successfully")
        except:
            time.sleep(2)
            error += 1
    else:
        machine.reset()

#Function to update time via network after initial time is set. This is not used due to power consumption concerns.
def updateTime():
    error = 0
    if error < 3:
        try:
            ntptime.settime()
            print("Time updated successfully")
        except:
            time.sleep(2)
            error += 1
    else:
        print("Could not update time - will try again later")

###### THIS IS THE START OF ACTUAL FUNCTIONALITY
#####
####
###
##
# Start procedure - set all displays to zero, connect to WiFi, indicate success, update time via network, proceed to clock functionality
print("START - sleep 2 seconds")
time.sleep(2)
print("connect to WiFi - sleep 1 second")
wlan_connect()
time.sleep(1)
print("update time via network - reset if this fails")
try:
    get_time_AIO()
except:
    try:
        get_time_backup()
    except:
        machine.reset()
time.sleep(1)
wlan_disconnect()
time.sleep(1)
print("connection success - setWlanSuccess indicator then sleep for 2 seconds")
setWlanSuccess()
time.sleep(2)
print("Set all displays to 0 then sleep for 2 seconds")
setALLZERO()
time.sleep(2)

###### Set some variables for use in the main loop
#####
####
###
##

#old time values for checking if the current value actually needs to be changed - this prevent the servos from making noise while not actually changing value.
#example: if dispaly currently shows 0 - you do not need to re-write 0 to it again. 
currentHourOld = 0
currentMinuteOld = 0

##### Main run loop - this is what actually does all the work
####
###
##
#
while True:
    #sleep for 1 second
    time.sleep(1)
    #do some definition for the time and apply the offset for selected timezone
    year, month, day, hour, mins, secs, weekday, yearday = time.localtime(time.time() + UTC_OFFSET)
    #create some variables that will be used later - apply formatting
    currentHour ="{}".format(hour%12)
    currentMinute = "{}".format(mins)
    #print the current time and resync value
    print("current time is: {}:{}".format(currentHour,currentMinute))
    
    # TIME IS CHANGED AND DISPLAYS ARE UPDATED HERE
    #Test if the hour has changed and only send changes if hour has changed
    if currentHour == currentHourOld:
        print("hour has not changed")
    else:
        #hour has changed - update the variable that tracks hour and update displays
        currentHourOld = currentHour
        if len(str(currentHour)) == 1:
            hoursTens.write(0)
            time.sleep(0.5)
            hoursOnes.write(int(currentHour) * degrees)
        else:
            hoursTens.write(int(currentHour[0]) * degrees)
            time.sleep(0.5)
            hoursOnes.write(int(currentHour[1]) * degrees)
                
    #test if minute has changed and only send changes if minute has changed
    time.sleep(0.5)
    if currentMinute == currentMinuteOld:
        print("minute has not changed")
    else:
        currentMinuteOld = currentMinute
        if len(currentMinute) == 1:
            minutesTens.write(0)
            time.sleep(0.5)
            minutesOnes.write(int(currentMinute) * degrees)
        else:
            minutesTens.write(int(currentMinute[0]) * degrees)
            time.sleep(0.5)
            minutesOnes.write(int(currentMinute[1]) * degrees)
