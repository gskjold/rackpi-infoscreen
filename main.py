#!/usr/bin/env python
import time
import Adafruit_SSD1306
import RPi.GPIO as GPIO
import subprocess

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

from config import Config

config = Config()
pages = config.pages

GPIO.setmode(GPIO.BCM)
GPIO.setup(config.led_pin, GPIO.OUT)
GPIO.setup(config.btn_pin, GPIO.IN)

# Menu Variables
menu_state = 0
menu_timer = 0
REBOOT_TIMEOUT = 4
SHUTDOWN_TIMEOUT = 8

do_reboot = 0
do_shutdown = 0

# 128x32 display with hardware I2C:
disp = Adafruit_SSD1306.SSD1306_128_32(rst=None)

# Initialize library.
disp.begin()

# Clear display.
disp.clear()
disp.display()

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
width = disp.width
height = disp.height
image = Image.new('1', (width, height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0,0,width,height), outline=0, fill=0)

# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = -2
top = padding
bottom = height-padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 2

# Load default font.
font = ImageFont.load_default()

# Alternatively load a TTF font.  Make sure the .ttf font file is in the same directory as the python script!
# Some other nice fonts to try: http://www.dafont.com/bitmap.php
# font = ImageFont.truetype('Minecraftia.ttf', 8)

GPIO.output(config.led_pin, GPIO.HIGH)

# Startup Info
draw.rectangle((0,0,width,height), outline=0, fill=0)
draw.text((x, top),    "--------------------", font=font, fill=255)
draw.text((x, top+12), " Infoscreen Started ", font=font, fill=255)
draw.text((x, top+24), "--------------------", font=font, fill=255)
disp.image(image)
disp.display()

time.sleep(5)

run = True
tick = 0
next_page = False
page = pages[0]
while run:
    tick += 1
    if tick > 127:
        tick = 0

    if tick % 8 == 0:
        next_page = True

    # Info Button pressed?
    if GPIO.input(config.btn_pin) == 0:
        if menu_timer >= SHUTDOWN_TIMEOUT:
            menu_state = 99
        elif menu_timer >= REBOOT_TIMEOUT:
            menu_state = 98
        else:
            next_page = True
        menu_timer = menu_timer+1
    elif next_page:
        menu_timer = 0
        menu_state += 1
        page = pages[menu_state]
        if not page:
            menu_state = 0
            page = pages[0]
        next_page = False

    # Draw a black filled box to clear the image.
    draw.rectangle((0,0,width,height), outline=0, fill=0)

    if menu_state < 90:
        ofs = 0
        for line in page.lines(3):
            draw.text((x, top+ofs), line, font=font, fill=255)
            ofs = ofs+12
    elif menu_state == 98:
        if GPIO.input(config.btn_pin) == 1:
            do_reboot = 1
            draw.text((x, top+12), "Performing Reboot...", font=font, fill=255)
            disp.image(image)
            disp.display()
            time.sleep(3)
            draw.rectangle((0,0,width,height), outline=0, fill=0)
        else:
            draw.text((x, top),    ".......Reboot......."     , font=font, fill=255)
            draw.text((x, top+12), "   Release Button   "   , font=font, fill=255)
            draw.text((x, top+24), "      To Reboot     "    , font=font, fill=255)
    elif menu_state == 99:
        if GPIO.input(config.btn_pin) == 1:
            do_shutdown = 1
            draw.text((x, top+12), "Shutting down.......", font=font, fill=255)
            disp.image(image)
            disp.display()
            time.sleep(3)
            draw.rectangle((0,0,width,height), outline=0, fill=0)
        else:
            draw.text((x, top),    "......Shutdown......"     , font=font, fill=255)
            draw.text((x, top+12), "   Release Button   "   , font=font, fill=255)
            draw.text((x, top+24), "    To Shutdown     "      , font=font, fill=255)

    disp.image(image)
    disp.display()

    if do_reboot == 1:
        cmd = "sudo reboot now"
        subprocess.Popen(cmd, shell = True)
        run = False
    elif do_shutdown == 1:
        cmd = "sudo shutdown now"
        subprocess.Popen(cmd, shell = True)
        run = False
    else:
        time.sleep(1)
