from bottle import *
from bottle import mako_view as view
import json
from threading import Thread, Timer
from time import sleep

REFRESH_RATE = 0.3


class Pin:
    def __init__(self, elm):
        self.pid = elm[0]
        self.channel = elm[1]
        self.name = elm[2]
        self.label = elm[3]
        self.status = elm[4]
        self.pud = False
        self.term = -1
        self.mode = -1
        self.meta = {}
        self.meta["callbacks"] = []

    def asdict(self):
        return {'pid': self.pid,
                'channel': self.channel,
                'name': self.name,
                'label': self.label,
                'status': self.status,
                'pud': self.pud,
                'term': self.term,
                'mode': self.mode}

PINS_DEFAULTS = [
        [1,     0, '3.3v',     'DC Power', 1],
        [2,     0, '5v',       'DC Power', 1],
        [3,     2, 'GPIO-02',  '',        -1],
        [4,     0, '5v',       'DC Power', 1],
        [5,     3, 'GPIO-03',  '',        -1],
        [6,     0, 'GND',      'Ground',   0],
        [7,     4, 'GPIO-04',  '',        -1],
        [8,    14, 'GPIO-14',  '',        -1],
        [9,     0, 'GND',      'Ground',   0],
        [10,   15, 'GPIO-15',  '',        -1],
        [11,   17, 'GPIO-17',  '',        -1],
        [12,   18, 'GPIO-18',  '',        -1],
        [13,   27, 'GPIO-27',  '',        -1],
        [14,    0, 'GND',      'Ground',   0],
        [15,   22, 'GPIO-22',  '',        -1],
        [16,   23, 'GPIO-23',  '',        -1],
        [17,    0, '3.3v',     'DC Power', 1],
        [18,   24, 'GPIO-24',  '',        -1],
        [19,   10, 'GPIO-10',  '',        -1],
        [20,    0, 'GND',      '',         0],
        [21,    9, 'GPIO-09',  '',        -1],
        [22,   25, 'GPIO-25',  '',        -1],
        [23,   11, 'GPIO-11',  '',        -1],
        [24,    8, 'GPIO-08',  '',        -1],
        [25,    0, 'GND',      'Ground',   0],
        [26,    7, 'GPIO-07',  '',        -1],
        [27,    0, 'ID_SD',    '-',       -1],
        [28,    0, 'ID_SC',    '-',       -1],
        [29,    5, 'GPIO-05',  '',        -1],
        [30,    0, 'GND',      'Ground',   0],
        [31,    6, 'GPIO-06',  '',        -1],
        [32,   12, 'GPIO-12',  '',        -1],
        [33,   13, 'GPIO-13',  '',        -1],
        [34,    0, 'GND',      'Ground',   0],
        [35,   19, 'GPIO-19',  '',        -1],
        [36,   16, 'GPIO-16',  '',        -1],
        [37,   26, 'GPIO-26',  '',        -1],
        [38,   20, 'GPIO-20',  '',        -1],
        [39,    0, 'GND',      'Ground',   0],
        [40,   21, 'GPIO-21',  '',        -1],
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
        if action == 'setstatus':
            GWGPIO.bypin(int(target)).status = int(data)
            return "set pin # %s status to %s: OK" % (target, data)
        if action == "setlabel":
            GWGPIO.bypin(int(target)).label = data
            return "set pin # %s label to %s: OK" % (target, data)
        if action == "setterm":
            GWGPIO.bypin(int(target)).term = int(data)
            return "set pin # %s term to %s: OK" % (target, data)


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
        self.MODE = None
        self.pins = PINS
        self.WARNINGS = True
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

    def remove_event_detect(self, channel):
        pin = self.gpio(channel)
        pin.meta["detect_active"] = False
        pin.meta["callbacks"] = []

    def add_event_callback(self, channel, callback):
        pin = self.gpio(channel)
        if not pin.meta["detect_active"]:
            raise Error("Add event detection using add_event_detect "
                        "first before adding a callback")
        pin.meta["callbacks"].append(callback)

    def gpio_function(self, channel):
        return self.gpio(channel).mode

    def setup(self, channels, direction, pull_up_down=20, initial=0):
        if type(channels) is not list:
            channels = [channels]
        for channel in channels:
            self.gpio(channel).mode = direction
            if pull_up_down == self.PUD_UP:
                self.gpio(channel).polarity = 0
            if pull_up_down == self.PUD_DOWN:
                self.gpio(channel).status = 0

    def wait_for_edge(self, channel, edge, bouncetime=None, timeout=None):
        # bouncetime its irrelevant on soft implementation (I hope)
        pin = self.gpio(channel)
        laststatus = pin.status
        pin.meta["timeout"] = False
        pin.meta["detect_active"] = True

        def dotimeout():
            pin.meta["timeout"] = True

        if timeout:
            Timer(float(timeout)/1000, dotimeout).start()

        while True:
            if pin.meta["timeout"] or not pin.meta["detect_active"]:
                pin.meta["timeout"] = False
                return
            sleep(0.01)  # <- might be too long
            if edge == self.RISING and pin.status == self.HIGH:
                break
            if edge == self.FALLING and pin.status == self.LOW:
                break
            if edge == self.BOTH and pin.status != laststatus:
                # means EITHER? .. I am not sure
                break
            laststatus = pin.status
        return channel

    def add_event_detect(self, channel, edge, callback=None, bouncetime=None):
        pin = self.gpio(channel)
        if pin.mode != 1:
            raise Error("You must setup() the GPIO channel as an input first")
        pin.meta["edge_detected"] = False
        pin.meta["detect_active"] = True
        if callback:
            pin.meta["callbacks"].append(callback)

        def watcher():
            if not pin.meta["detect_active"]:
                return
            while pin.meta["detect_active"]:
                if self.wait_for_edge(channel, edge) == channel:
                    pin.meta["edge_detected"] = True
                    if len(pin.meta["callbacks"]) > 0:
                        for cb in pin.meta["callbacks"]:
                            cb(channel)
                if bouncetime:
                    sleep(float(bouncetime)/1000)
                    # not sure if I got the bouncetime concept correctly

        t = Thread(target=watcher)
        t.daemon = True
        t.start()

    def event_detected(self, channel):
        pin = self.gpio(channel)
        if not pin.meta["detect_active"]:
            raise Error("no event active on this channel")
        if pin.meta["edge_detected"]:
            pin.meta["edge_detected"] = False
            return True
        return False

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
            if pin.mode == -1:
                raise Error("You must setup() the GPIO channel first ")
            if value == self.HIGH:
                pin.status = 1
            elif value == self.LOW:
                pin.status = 0
            else:
                raise Error("The channel sent is invalid on a Raspberry Pi")

    def input(self, channel):
        if self.gpio(channel).mode != 0:
            return self.gpio(channel).status
        else:
            raise Error("You must setup() the GPIO channel first")

    def setwarnings(*k):
        pass

    def getmode(self):
        return self.MODE

    def setmode(self, mode):
        self.MODE = mode


class Error(Exception):
    def __init__(self, value):
        print value
        self.value = value

    def __str__(self):
        return repr(self.value)
