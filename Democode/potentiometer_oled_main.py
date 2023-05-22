from machine import Pin, ADC, I2C
from ssd1306 import SSD1306_I2C
import utime


# define width and height of OLED display
WIDTH = 128
HEIGHT = 64

# initializing OLED display
i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=200000)
oled = SSD1306_I2C(WIDTH, HEIGHT, i2c)
oled.fill(0) # clear screen

# Define ADC instance
pot = ADC(Pin(26))

#define remap function to map the potentiometer's value from 288-65535 to 0 to 127
def _mapping(x, in_min, in_max, out_min, out_max):
    return int( (x - in_min) * ( out_max - out_min) / (in_max - in_min) + out_min)

# loop
while True:
    x_pos = _mapping(pot.read_u16(), 288, 65535, 0, 127)
    print(x_pos)
    oled.hline(x_pos, 10, 15, 1)
    oled.fill_rect(x_pos, 15, 5, 5, 1)
    oled.rect(x_pos, 15, 15, 15, 1)
    oled.rect(x_pos, 40, 15, 15, 1)
    oled.hline(x_pos, 35, 15, 1)
    #oled.vline(x_pos, 35, 15,1)
    oled.fill_rect(x_pos, 40, 5, 5, 1)
    oled.show()
    utime.sleep(0.2)
    oled.fill(0)
    

    