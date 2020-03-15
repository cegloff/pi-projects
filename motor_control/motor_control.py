from gpiozero import Motor
from time import sleep

motorR = Motor(forward=4, backward=18)
motorL = Motor(forward=17, backward=27)



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



