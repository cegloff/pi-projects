import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
from time import sleep
import subprocess
import syslog
from datetime import datetime
import os

#################################################################################################
# Cron command to run this script every minute                                                  #
# */1 * * * * /usr/bin/python3 /scripts/ads1115/get_bat.py >/dev/null 2>&1                      #
#                                                                                               #
# The code for interfacing with the ADS1115 came from the Adafruit example                      #
# located at: https://learn.adafruit.com/adafruit-4-channel-adc-breakouts/python-circuitpython  #
#################################################################################################


def get_battery():
    # Get the voltage of the battery by useing the ADS1115
    i2c = busio.I2C(board.SCL, board.SDA)
    ads = ADS.ADS1115(i2c)
    avg_bat = 0

    # Take three samples and average them
    for i in range(4):
        chan = AnalogIn(ads, ADS.P0)
        # Measuring with multimeter 2.043 was the correct multiplier for my splitter
        # this value should be updated for each build
        current_voltage = chan.voltage * 2.043
        avg_bat = avg_bat + current_voltage
    avg_bat = avg_bat/4

    # Return the average of the three battery samples
    return(avg_bat)


def os_announce(message):
    # Use wall and xmessage to announce any message passed to the function
    # to all logged in users.
    command = "/usr/bin/wall"
    subprocess.call([command, message])
    os.environ["DISPLAY"] = ':0.0'
    os.environ["XAUTHORITY"] = '/home/pi/.Xauthority'
    command = "xmessage"
    subprocess.call([command, message])


def shutdown_system(message):
    # command = "shutdown"
    # arg1 = "-h"
    # arg2 = "-t 120"
    # subprocess.call([command, arg1, arg2, message])
    os.system('systemctl poweroff')


if __name__ == "__main__":
    current_bat = get_battery()
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if current_bat <= 3.1:
        # If the battery voltage is critical send a shutdown command and then
        # use wall to send a message to all users finally log the voltage and
        # warning to syslog
        message = 'Voltage is Critial.  System will is shutting down. Current Voltage = ' + \
            str(current_bat)
        syslog.syslog("[Critical] Battery Voltage is: %s" % current_bat)
        os_announce(message)
        shutdown_system(message)
    elif current_bat < 3.2 and current_bat > 3.1:
        # If the battery voltage is low use wall to send a message to all users
        # then log the voltage and warning to syslog
        message = 'BATTERY IS LOW! Current Voltage = ' + str(current_bat)
        syslog.syslog("[Error] Battery Voltage is: %s" % current_bat)
        os_announce(message)
    else:
        # If the battery isn't critical log the voltage every 5 minutes
        minute = int(datetime.now().strftime('%M')) % 5
        if minute == 0:
            syslog.syslog("Battery Voltage is: %s" % current_bat)
