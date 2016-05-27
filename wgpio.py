from bottle import *
from bottle import mako_view as view
import json
from threading import Thread
from time import sleep

REFRESH_RATE = 0.3


class Pin:
    def __init__(self, elm):
        self.pid = elm[0]
        self.device = elm[1]
        self.name = elm[2]
        self.status = elm[3]
        self.label = elm[4]
        self.polarity = elm[5]
        self.channel = elm[6]

    def asdict(self):
        return {
                'pid': self.pid,
                'device': self.device,
                'name': self.name,
                'status': self.status,
                'label': self.label,
                'polarity': self.polarity,
                'channel': self.channel,
            }

# defaults pin, device, name, status, label, channel_num
PINS_DEFAULTS = [
        [1,  'none', '3.3v', '', 'DC Power', -1, 0],
        [2,  'none', '5v', '', 'DC Power', -1, 0],
        [3,  'none', 'GPIO-02', -1, '', -1, 2],
        [4,  'none', '5v', '', 'DC Power', -1, 0],
        [5,  'none', 'GPIO-03', -1, '', -1, 3],
        [6,  'none', 'GND', '', 'Ground', -1, 0],
        [7,  'none', 'GPIO-04', -1, '', -1, 4],
        [8,  'none', 'GPIO-14', -1, '', -1, 14],
        [9,  'none', 'GND', '', 'Ground', -1, 0],
        [10, 'none', 'GPIO-15', -1, '', -1, 15],
        [11, 'none', 'GPIO-17', -1, '', -1, 17],
        [12, 'none', 'GPIO-18', -1, '', -1, 18],
        [13, 'none', 'GPIO-27', -1, '', -1, 27],
        [14, 'none', 'GND', '', 'Ground', -1, 0],
        [15, 'none', 'GPIO-22', -1, '', -1, 22],
        [16, 'none', 'GPIO-23', -1, '', -1, 23],
        [17, 'none', '3.3v', '', 'DC Power', -1, 0],
        [18, 'none', 'GPIO-24', -1, '', -1, 24],
        [19, 'none', 'GPIO-10', -1, '', -1, 10],
        [20, 'none', 'GND', '', '', -1, 0],
        [21, 'none', 'GPIO-09', -1, '', -1, 9],
        [22, 'none', 'GPIO-25', -1, '', -1, 25],
        [23, 'none', 'GPIO-11', -1, '', -1, 11],
        [24, 'none', 'GPIO-08', -1, '', -1, 8],
        [25, 'none', 'GND', '', 'Ground', -1, 0],
        [26, 'none', 'GPIO-07', -1, '', -1, 7],
        [27, 'none', 'ID_SD', '', '', -1, 0],
        [28, 'none', 'ID_SC', '', '', -1, 0],
        [29, 'none', 'GPIO-05', -1, '', -1, 5],
        [30, 'none', 'GND', '', 'Ground', -1, 0],
        [31, 'none', 'GPIO-06', -1, '', -1, 6],
        [32, 'none', 'GPIO-12', -1, '', -1, 12],
        [33, 'none', 'GPIO-13', -1, '', -1, 13],
        [34, 'none', 'GND', '', 'Ground', -1, 0],
        [35, 'none', 'GPIO-19', -1, '', -1, 19],
        [36, 'none', 'GPIO-16', -1, '', -1, 16],
        [37, 'none', 'GPIO-26', -1, '', -1, 26],
        [38, 'none', 'GPIO-20', -1, '', -1, 20],
        [39, 'none', 'GND', '', 'Ground', -1, 0],
        [40, 'none', 'GPIO-21', -1, '', -1, 21],
    ]

PINS = [Pin(elm=e) for e in PINS_DEFAULTS]

# the following might not be a good approach. I dont know any other way.
# GWGPIO is a GLobal that will have the WGPIO class once initialized
GWGPIO = None


@get('/')
@view('main')
def main():
    return dict(pins=PINS)


@get('/out')
def out():
    sleep(REFRESH_RATE)
    return json.dumps([pin.asdict() for pin in PINS])


@get('/in/<cmd>')
def ain(cmd):
    if not GWGPIO:
        return 'Error: WGPIO was not initialised'
    return process(cmd)


@route('/css/<filepath:path>')
def server_static_css(filepath):
    return static_file(filepath, root='css')


@route('/js/<filepath:path>')
def server_static_js(filepath):
    return static_file(filepath, root='js')


@route('/media/<filepath:path>')
def server_static_media(filepath):
    return static_file(filepath, root='media')


def process(cmd):
    commands = cmd.split(',')
    for command in commands:
        target, action, data = command.split(':')
        if action == 'sethigh':
            GWGPIO.bypin(int(target)).status = GWGPIO.HIGH
        if action == 'setlow':
            GWGPIO.bypin(int(target)).status = GWGPIO.LOW
        if action == "setlabel":
            GWGPIO.bypin(int(target)).label = int(data)
        if action == "setpolarity":
            GWGPIO.bypin(int(target)).polarity = int(data)


def runweb():
    run(host='0.0.0.0', port=8000, debug=True, server='cherrypy', quiet=True)

webt = Thread(target=runweb)
webt.daemon = True
webt.start()


class WGPIO:
    def __init__(self):
        global PINS, GWGPIO
        self.BCM = 11
        self.UNKNOWN = -1
        self.HARD_PWM = 43
        self.LOW = 0
        self.I2C = 42
        self.SERIAL = 40
        self.BOTH = 33
        self.SPI = 41
        self.RPI_REVISION = 3
        self.OUT = 0
        self.HIGH = 1
        self.VERSION = "wgpio v0.2"
        self.RISING = 31
        self.IN = 1
        self.FALLING = 32
        self.PUD_UP = 22
        self.PUD_OFF = 20
        self.PUD_DOWN = 21
        self.BOARD = 10
        self.pins = PINS
        self.MODE = None
        self.PUSH = 'push'
        self.LED = 'led'
        GWGPIO = self  # I have the feeling that this is an ugly approach :(

    def gpio(self, channel):
        if self.MODE == self.BCM:
            if channel == 0:
                raise Error('Channel 0 does not exist')
            for pin in self.pins:
                if pin.channel == channel:
                    return pin
            raise Error('Unknown Channel')
        elif self.MODE == self.BOARD:
            return bypin(channel)
        else:
            raise Error("MODE not set (BCM or BOARD)")

    def bypin(self, number):
        if number - 1 > len(self.pins):
            raise Error('Unknown PIN num %s' % number)
        if number <= 0:
            raise Error('invalid PIN %s' % number)
        if self.pins[number - 1].channel > 0:
            return self.pins[number - 1]
        else:
            raise Error('Pin %s is not an IO number' % number)

    def event_detected(*k):
        pass

    def remove_event_detect(*k):
        pass

    def add_event_callback(*k):
        pass

    def gpio_function(*k):
        pass

    def setup(self, channels, direction, pull_up_down=20, initial=0):
        if type(channels) is not list:
            channels = [channels]
        for channel in channels:
            if direction == self.OUT:
                self.gpio(channel).device = self.LED
            if direction == self.IN:
                self.gpio(channel).device = self.PUSH

    def wait_for_edge(*k):
        pass

    def cleanup(self, channels=False):
        if not channels:
            global PINS
            PINS = [Pin(elm=e) for e in PINS_DEFAULTS]
            return
        if type(channels) is not list:
            channels = [channels]
        for channel in channels:
            pin = self.gpio(channel)
            PINS[pin.pid - 1] = Pin(elm=PINS_DEFAULTS[pin.pid - 1])

    def output(self, channels, value):
        if type(channels) is not list:
            channels = [channels]
        for channel in channels:
            pin = self.gpio(channel)
            if pin.device == "none":
                raise Error("Channel %s is not setup" % channel)
            if value == self.HIGH:
                pin.status = "on"
            elif value == self.LOW:
                pin.status = "off"
            else:
                raise Error("%s is an invalid value" % value)

    def input(*k):
        pass

    def setwarnings(*k):
        pass

    def getmode(self):
        return self.MODE

    def setmode(self, mode):
        self.MODE = mode

    def add_event_detect(*k):
        pass


class Error(Exception):
    def __init__(self, value):
        print value
        self.value = value

    def __str__(self):
        return repr(self.value)
