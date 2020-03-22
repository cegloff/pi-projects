#!/usr/bin/python3

#!/usr/bin/python3
import RPi.GPIO as GPIO
import time
from time import sleep

motorRF = 17
motorRR = 27
motorLF = 23
motorLR = 24
enableL = 12
enableR = 13
left_speed_multiplier = 2
right_speed_multiplier = .9
motor_pins = [motorRF,motorRR,motorLF,motorLR,enableL,enableR]

speed = 20
GPIO.setmode(GPIO.BCM)
GPIO.setup(motor_pins, GPIO.OUT)
left_speed = GPIO.PWM(enableL, 1000)
right_speed = GPIO.PWM(enableR, 1000)
left_speed.start(speed * left_speed_multiplier)
right_speed.start(speed * right_speed_multiplier)


def forward():
    GPIO.output(motorRF, GPIO.HIGH)
    GPIO.output(motorLF, GPIO.HIGH)
    GPIO.output(motorRR, GPIO.LOW)
    GPIO.output(motorLR, GPIO.LOW)

def reverse():
    GPIO.output(motorRF, GPIO.LOW)
    GPIO.output(motorLF, GPIO.LOW)
    GPIO.output(motorRR, GPIO.HIGH)
    GPIO.output(motorLR, GPIO.HIGH)


def stop():
    GPIO.output(motorRF, GPIO.LOW)
    GPIO.output(motorRR, GPIO.LOW)
    GPIO.output(motorLF, GPIO.LOW)
    GPIO.output(motorLR, GPIO.LOW)

def speed(speed):
    if speed < 20:
        speed = 20
    if speed > 50:
        speed = 50
    left_speed.ChangeDutyCycle(speed * left_speed_multiplier)
    right_speed.ChangeDutyCycle(speed * right_speed_multiplier)


if __name__ == "__main__":
    reverse()
    time.sleep(3)
    speed(40)
    sleep(3)
    stop()
    GPIO.cleanup()
   

