
class WGPIO:
    def __init__(self):
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
        self.VERSION = "0.0.2"
        self.RISING = 31
        self.IN = 1
        self.FALLING = 32
        self.PUD_UP = 22
        self.PUD_OFF = 20
        self.PUD_DOWN = 21
        self.BOARD = 10

    def event_detected(*k):
        pass

    def remove_event_detect(*k):
        pass

    def add_event_callback(*k):
        pass

    def gpio_function(*k):
        pass

    def setup(*k):
        pass

    def wait_for_edge(*k):
        pass

    def cleanup(*k):
        pass

    def output(*k):
        pass

    def input(*k):
        pass

    def setwarnings(*k):
        pass

    def getmode(*k):
        pass

    def setmode(*k):
        pass

    def add_event_detect(*k):
        pass
