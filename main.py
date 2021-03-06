#!/usr/bin/env python
import time
from luma.core.interface.serial import i2c, spi
from luma.core.render import canvas
from luma.oled.device import ssd1306
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

serial = i2c(port=1, address=0x3C)
device = ssd1306(serial, width=config.width, height=config.height, rotate=config.rotate)

width = config.width
height = config.height
padding = -2
top = padding
bottom = height-padding
x = 2
font = ImageFont.load_default()

# Alternatively load a TTF font.  Make sure the .ttf font file is in the same directory as the python script!
# Some other nice fonts to try: http://www.dafont.com/bitmap.php
# font = ImageFont.truetype('Minecraftia.ttf', 8)

GPIO.output(config.led_pin, GPIO.HIGH)

# Startup Info
with canvas(device) as draw:
    draw.rectangle((0,0,width,height), outline=0, fill=0)
    draw.text((x, top),    "--------------------", font=font, fill=255)
    draw.text((x, top+12), " Infoscreen Started ", font=font, fill=255)
    draw.text((x, top+24), "--------------------", font=font, fill=255)

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
        menu_state += 1
        if len(pages) > menu_state:
            page = pages[menu_state]
        else:
            menu_state = 0
            page = pages[0]
        next_page = False
    else:
        menu_timer = 0

    if menu_state < 90:
        ofs = 0
        with canvas(device) as draw:
            draw.rectangle((0,0,width,height), outline=0, fill=0)
            for line in page.lines(3):
                draw.text((x, top+ofs), line, font=font, fill=255)
                ofs = ofs+12
    elif menu_state == 98:
        with canvas(device) as draw:
            if GPIO.input(config.btn_pin) == 1:
                do_reboot = 1
                draw.text((x, top+12), "Performing Reboot...", font=font, fill=255)
                time.sleep(3)
                draw.rectangle((0,0,width,height), outline=0, fill=0)
            else:
                draw.text((x, top),    ".......Reboot......."     , font=font, fill=255)
                draw.text((x, top+12), "   Release Button   "   , font=font, fill=255)
                draw.text((x, top+24), "      To Reboot     "    , font=font, fill=255)
    elif menu_state == 99:
        with canvas(device) as draw:
            if GPIO.input(config.btn_pin) == 1:
                do_shutdown = 1
                draw.text((x, top+12), "Shutting down.......", font=font, fill=255)
                time.sleep(3)
                draw.rectangle((0,0,width,height), outline=0, fill=0)
            else:
                draw.text((x, top),    "......Shutdown......"     , font=font, fill=255)
                draw.text((x, top+12), "   Release Button   "   , font=font, fill=255)
                draw.text((x, top+24), "    To Shutdown     "      , font=font, fill=255)

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
