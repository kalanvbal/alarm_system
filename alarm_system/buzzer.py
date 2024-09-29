from gpiozero import Buzzer
from time import sleep

buzzer = Buzzer(5)

while True:
    buzzer.on()
    
    