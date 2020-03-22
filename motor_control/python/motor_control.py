from gpiozero import Motor
from time import sleep
from gpiozero import PWMLED

motorR = Motor(forward=23, backward=24)#, pwm=False)
motorL = Motor(forward=17, backward=27)#, pwm=False)

enable1 = PWMLED(12)
enable2 = PWMLED(13)
## Enable values set the speed of the motors.
## For the current 12v setup, this is a min 15 and max 65
enable1.value = 35 / 100
enable2.value = 35 / 100

def forward():
# while True:
    motorR.forward()
    motorL.forward()

def stop():
    motorR.stop()
    motorL.stop()


def reverse():
    motorR.backward()
    motorL.backward()

if __name__ == "__main__":
    reverse()
    sleep(5)
    stop()

