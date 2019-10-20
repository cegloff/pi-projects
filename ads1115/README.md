# Raspberry Pi batery checks

## Maintainer
Name: Chris Egloff


## Summary
Quick script to be used with Raspberry pi to utilize an ADS1115 ADC to check the voltage of a battery.  I'm using a lithium ion battery so am checking to see if the voltage is above 3.2V.  
If the voltage is greater than 3.2V then log the voltage once every five minutes.  If the voltage 
is less than 3.2V use wall to announce to all logged in users that it's low and log the alert.

I use a cronjob to run this script every minute and then take action according to the
battery voltage.


## Execution Instructions
Cron command to run this script every minute, assuming that you have the
script copied to /scripts/ads1115/get_bat.py 

*/1 * * * * /usr/bin/python3 /scripts/ads1115/get_bat.py >/dev/null 2>&1     



### Outputs
If the voltage is greater than 3.2V then log the voltage once every five minutes.  If the voltage 
is less than 3.2V use wall to announce to all logged in users that it's low and log the alert.


## File Structure
### subnet.py:
The code for interfacing with the ADS1115 came from the Adafruit example
located at: https://learn.adafruit.com/adafruit-4-channel-adc-breakouts/python-circuitpython

## Original Sources With Links
N/A

## Dependencies
Running this template requires python 3 and the adafruit python library adafruit_ads1x15

