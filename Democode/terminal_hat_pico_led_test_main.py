from machine import Pin
from utime import sleep


leds = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21,22, 26, 27, 28]
lights = []
light = {}
for led in leds:
    light[led] = Pin(led, Pin.OUT)
    lights.append(light[led])
    print(lights)

while True:
    for i in lights:
        i.value(1)
        sleep(0.1)
        
    for i in lights:
        i.value(0)
        sleep(0.1)
        