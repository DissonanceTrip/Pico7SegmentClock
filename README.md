# Pico7SegmentClock
micropython code for Pico W to control a "rack driven 7 segment display" clock

# Hardware
Rack Driven 7 Segment Display by Engineezy: https://engineezy.com/products/the-rack-driven-7-segment-display

Raspberry Pi Pico W: https://www.raspberrypi.com/products/raspberry-pi-pico/?variant=raspberry-pi-pico-w

Servo board (for power/easy hookup): https://www.waveshare.com/pico-servo-driver.htm

12v 5a power supply: get one from pretty much anywhere

wire to connect the power supply to the waveshare board: whatever works

some MG995 servos: I got some off amazon - https://www.amazon.com/Control-Angle180-Digital-Torque-Helicopter/dp/B07NQJ1VZ2

# Code
The Pico W will need 2 files:
1) main.py - this does the majority of the work
2) secrets.py - this will hold your wifi name and password

# Extra files
I have included a few extra files to make this whole process easier:
1) degreetest.py - makes it easy to figure out how much the servos need to rotate for each number
2) Explain.txt - this file has a lot of explaination for what everything does and how the code works

# IMPORTANT NOTE:
You will need to change variables in the main.py and secrets.py in order for this to work properly. It will NOT work if you just copy everything over and make no changes.

# How it works in human readable format
The code functions as described:

Once connected to power, the Pico will sleep for 3 seconds.

Next, the Pico will set all the servo positions to 0 degrees which should correspond with the number 0 on each display. 

Next, the Pico will connect to the wifi network, as defined, then sleep for 2 seconds.

Next, the Pico will set the servo positions to a defined number/pattern (default is 1337 because I'm funny) then sleep for 2 seconds. This indicates that wireless connection has succeeded.

Next, utilizing the wireless connection, some API calls will be made to establish what UTC offset is needed for the current location then sync time from public NTP server. This has a primary and a backup function.

Next, after sleeping for 1 second, the wireless chip will be disabled to conserve power (and avoid any issues with overdrawing the servo board), then sleep again for 1 second.

Next, the current actual local time will be calculated utilizing the UTC offset, time will be formatted, and the servos will be set to reflect the current time. This runs in a loop that will update the displays to match the time as it changes.

Every hour of operation, the wireless chip will be re-enabled, it will connect to wifi, resync the RTC via NTP, and diable the wireless chip after it is done. This is to ensure the time is kept as accurate as possible, but it is not really neccessary.

# Things you can/should change (this is documented in code comments as well)
I was pretty agressive with the sleep values between servo movements and checks - you could reduce these values without issue, but I do recommend leaving some time between movements to prevent overloading anything

You can statically set the UTC_OFFSET value for your timezone if you want. I had issues with this so it gets this value via APIs instead. If you statically set it, remove the methods that would update it.

The degrees variable is used to move the servos a set amount. You can use the degreetest.py code to find this value and change it for your particular setup.

You SHOULD to change the pin values to match where you have your servos plugged in (or just plug them in to the same pins I did)

You MUST update the secrets.py file with your wifi name (ssid) and password. If you don't do this, you don't get wifi :( 

# Known issues as of 30/10/2024
Not sure why, but sometimes the code doesn't convert to 12 hour time properly and you end up with 24 hour time: such as 13:00 instead of 01:00 I have no idea why this happens as it only does it sometimes.

Sometimes there is issues reconnecting the wifi during operation to resync the time - if you run into this issue you can either remove those checks entirely or just ignore it. Everything should keep working. 


# Credit and Thanks
Credit and Thanks to Engineezy (linked above under hardware) for the models and build instructions. 10/10 I love your work <3

Credit and Thanks to redoxcode [https://github.com/redoxcode/micropython-servo] for the micropython-servo library for servo control. 10/10 made this super easy <3

Credit to the Get Started Guide for the wlan_connect() method: https://projects.raspberrypi.org/en/projects/get-started-pico-w/2

Credit and Thanks to Bhavesh Kakwani for this guide that I ended up with remnants of in the final code: https://bhave.sh/micropython-ntp/

Thanks to worldtimeapi.org and ipify.org and timeapi.io for having good (FREE!!!!) APIs that made this easier and more generally usable <3

Thanks to everyone on the Raspbery Pi Forum that helped me troubleshoot a, probably self-imposed, issue with this whole thing <3

Thanks to a number of random forum posts from 2017 for assorted troubleshooting during the times where I was overcomplicating things instead of just doing it a non-stupid way :P 
