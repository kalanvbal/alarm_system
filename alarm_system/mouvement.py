from gpiozero import MotionSensor, LED
from signal import pause
options = ['1', '2', '3', 'A',
           '4', '5', '6', 'B',
           '7', '8', '9', 'C',
           '*', '0', '#', 'D']
lignesGPIO = [26, 19, 13, 6]
colonnesGPIO = [5, 22, 27, 17]

code = '12312'
pir = MotionSensor(4)
led = LED(22)

while True:
    if pir.value == 1:
        led.on()
        print("1")
    else:
        led.off()
        print("0")