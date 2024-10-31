# Pico7SegmentClock
micropython code for Pico W to control a "rack driven 7 segment display" clock

# Hardware
Rack Driven 7 Segment Display by Engineezy: https://engineezy.com/products/the-rack-driven-7-segment-display

Raspberry Pi Pico W: https://www.raspberrypi.com/products/raspberry-pi-pico/?variant=raspberry-pi-pico-w

Servo board (for power/easy hookup): https://www.waveshare.com/pico-servo-driver.htm

You can use a different board or wire it up yourself - The servo control code can work with all methods!

Wire to connect the power supply to the servo board (if needed)

12v 5a power supply: get one from pretty much anywhere

some MG995 180degree servos: I got some off amazon - https://www.amazon.com/Control-Angle180-Digital-Torque-Helicopter/dp/B07NQJ1VZ2

# Disclaimer
Many of these Pico servo boards are not intended for use with a Pico W as the wireless chip draws additional power. Running the servos while the wireless chip is active can cause damage to the Pico W.

This code is adjusted to only have the wireless chip active during the initial few seconds that the system is powered up. This SHOULD be fine, but I accept no responsibility if your Pico W gets fried or burns down your house.

I've been running this code for long periods of time with no issues - your experience may vary. Use at your own risk.

# Code
The Pico W will need 2 files:
1) main.py - this does the majority of the work
2) secrets.py - this will hold your WiFi name and password

# Extra files
I have included a few extra files to make this whole process easier:
1) degreetest.py - makes it easy to figure out how much the servos need to rotate for each number
2) Explain.txt - this file has a lot of extra details that you don't need

# IMPORTANT NOTE:
You will need to change variables in the main.py and secrets.py in order for this to work properly. It will NOT work if you just copy everything over and make no changes.

# How it works in human readable format
The code functions as described:

Once connected to power, the Pico will sleep for 3 seconds.

Next, the Pico will set all the servo positions to 0 degrees which should correspond with the number 0 on each display. Sleep for 4 seconds.

Next, the Pico will connect to the WiFi network, as defined, then sleep for 1 second.

Next, utilizing the wireless connection, some API calls will be made to establish what UTC offset is needed for the current location then sync time from public NTP server. This has a primary and a backup function.

Next, the wireless chip will be disabled to conserve power (and avoid any issues with overdrawing the servo board), then sleep again for 2 seconds.

Next, the Pico will set the servo positions to a defined number/pattern (default is 1337 because I'm funny) then sleep for 2 seconds. This indicates that wireless connection has succeeded.

Next, the current actual local time will be calculated utilizing the UTC offset, time will be formatted, and the servos will be set to reflect the current time. This runs in a loop that will update the displays to match the time as it changes.


# Things you can/should change (this is documented in code comments as well)
I was pretty aggressive with the sleep values between servo movements and checks - you could reduce these values without issue, but I do recommend leaving some time between movements to prevent overloading anything

You can statically set the UTC_OFFSET value for your timezone if you want. I had issues with this so it gets this value via APIs instead. If you statically set it, remove the methods that would update it.

The degrees variable is used to move the servos a set amount. You can use the degreetest.py code to find this value and change it for your particular setup.

You SHOULD to change the pin values to match where you have your servos plugged in (or just plug them in to the same pins I did)

You MUST update the secrets.py file with your WiFi name (ssid) and password. If you don't do this, you don't get WiFi :( 

# Known issues as of 31/10/2024
Setting a single static value for the rotation of ALL the servos sometimes doesn't work perfectly. Some displays may move more/less than others. This is primarily an issue of the physical properties of the displays. I plan to revise the code, and include it as a alternative version, to allow you to set individual degree values for each servo to compensate for this. This will be released later - in the meantime, the current method works well enough in most cases if your prints are consistent! Be sure to use the degreetest.py code to find what works best for you!


# Troubleshooting
If you run into issues, I recommend tinkering with it to try to figure it out! (That's half the fun of the whole project!)

If you have any particular bugs or improvements, please feel free to open an issue or pull request and I'll take a look.

I will not troubleshoot hardware issues here - please consult other forums for hardware issues


# Credit and Thanks
Credit and Thanks to Engineezy https://engineezy.com/pages/about for the models and build instructions. 10/10 I love your work <3

Credit and Thanks to redoxcode https://github.com/redoxcode/micropython-servo for the micropython-servo library for servo control. 10/10 made this super easy

Credit to the Get Started Guide for the wlan_connect() method: https://projects.raspberrypi.org/en/projects/get-started-pico-w/2

Credit and Thanks to Bhavesh Kakwani for this guide that I ended up with remnants of in the final code: https://bhave.sh/micropython-ntp/

Thanks to worldtimeapi.org and ipify.org and timeapi.io for having good (FREE!!!!) APIs that made this easier and more generally usable

Thanks to everyone on the Raspberry Pi Forum that helped me troubleshoot a, probably self-imposed, issue with this whole thing <3

Thanks to a number of random forum posts from 2017 for assorted troubleshooting during the times where I was over-complicating things instead of just doing it a non-stupid way :P 
