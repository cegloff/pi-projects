from gpiozero import Motor
from time import sleep
from gpiozero import PWMLED

motorR = Motor(forward=4, backward=18, pwm=False)
motorL = Motor(forward=17, backward=27, pwm=False)

enable1 = PWMLED(12)
enable2 = PWMLED(13)
enable1.value = 50 / 100
enable2.value = 50 / 100

def forward():
# while True:
    motorR.forward()
    motorL.forward()

def stop():
    motorR.stop()
    motorL.stop()


def reverse():
    motorR.reverse()
    motorL.reverse()



