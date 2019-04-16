from page import Page
from cards.hostname import CardHostname
from cards.uptime import CardUptime
from cards.cpu import CardCpu
from cards.mem import CardMem

class Config:
    def __init__(self):
        self.pages = {}
        self.pages.append(Page(CardHostname(), CardUptime(), CardCpu(), CardMem()))

        self.led_pin = 23
        self.btn_pin = 20
