# code.py - Macarboard ( Raspberry pi pico, CircuitPython )
# By Martavgeek and Platots

# ====================== Libraries ========================= #
import time  
import board   
import busio
import digitalio 
import usb_hid 
import adafruit_ssd1306 

# ================ Config ================== #
SDA_PIN = board.GP4
SCL_PIN = board.GP5

BUTTON_PINS = (board.GP10, board.GP11, board.GP12, board.GP13, board.GP14)
BUTTON_NAMES = ("key1","key2","key3", "GAS", "BRAKE")

AS5600_ADDR = 0x36
OLED_ADDR = 0x3C
OLED_WIDTH = 128
OLED_HEIGHT = 64
I2C_FREQ = 400_000

LOOP_DELAY = 0.1

# AS5600 Registers 
REG_STATUS = 0x0B
REG_RAW_ANGLE = 0x0C
REG_ANGLE = 0x0E
REG_AGC = 0x1A
REG_MAGNITUDE = 0x1B

# Init
def init_i2c():
    # Initialize I2C bus
    return busio.I2C(SCL_PIN, SDA_PIN, frequency=I2C_FREQ)

def init_buttons():
    #Set up button pins as inputs LOW
    buttons = []
    for pin in BUTTON_PINS:
        b = digitalio.DigitalInOut(pin)
        b.direction = digitalio.Direction.INPUT
        b.pull = digitalio.Pull.UP
        buttons.append(b)
    return buttons

def init_display(i2c):
    # Initialize display
    display = adafruit_ssd1306.SSD1306_I2C(OLED_WIDTH, OLED_HEIGHT, i2c, addr=OLED_ADDR)
    display.fill(0)
    display.show()
    return display

def init_sensor(i2c):
    # Initialize AS5600 sensor
    if AS5600_ADDR not in scan_i2c(i2c):
        raise RuntimeError("AS5600 sensor not found on I2C bus")
    detected, too_weak, too_strong = read_magnet_status(i2c)
    print("Magnet status - Detected: {}, Too Weak: {}, Too Strong: {}".format(detected, too_weak, too_strong))


# I2C
def scan_i2c(i2c):
    while not i2c.try_lock():
        pass
    try:
        return i2c.scan()
    finally:
        i2c.unlock()

def read_register(i2c, addr, reg, lenght):
    buf = bytearray(lenght)
    while not i2c.try_lock():
        pass
    try:
        i2c.writeto_then_readfrom(addr, bytes([reg]), buf)
    finally:
        i2c.unlock()
    return buf


# AS5600 
def read_raw_angle(i2c):
    buf = read_register(i2c, AS5600_ADDR, REG_RAW_ANGLE, 2)
    return ((buf[0] << 8) | buf[1]) & 0x0FFF

def read_magnet_status(i2c):
    status = read_register(i2c, AS5600_ADDR, REG_STATUS, 1)[0]
    return bool(status & 0x20), bool(status & 0x10), bool(status & 0x40)

def angle_to_axis(raw_angle):
    pass
    
# Buttons 
def read_buttons(buttons):
    return tuple(not b.value for b in buttons)    

# Display 
def update_display(display, lines):
    pass

# HID
def send_board_report(axis, button_states):
    pass

### main ###
def main():
    i2c= init_i2c()
    buttons = init_buttons()
    print("I2C devices: ", [hex(addr) for addr in scan_i2c(i2c)])
    display = init_display(i2c)

    while True:
        time.sleep(LOOP_DELAY)

main()
