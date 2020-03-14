from gpiozero import Motor
from time import sleep

motorR = Motor(forward=4, backward=18)
motorL = Motor(forward=17, backward=27)


# while True:
motorR.forward()
sleep(2)
motorR.backward()
sleep(2)
motorR.stop()

motorL.forward()
sleep(2)
motorL.backward()
sleep(2)
motorL.stop()