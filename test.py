from wgpio import WGPIO

GPIO = WGPIO()
GPIO.setmode(GPIO.BCM)
# test detection
# GPIO.setup(11, GPIO.IN)
# GPIO.add_event_detect(11, GPIO.RISING, bouncetime=500)


# def f1(channel):
#    print "Pressed Channel F1 " + str(channel)


# def f2(channel):
#    print "Pressed Channel h2" + str(channel)

# GPIO.add_event_callback(11, f1)
# GPIO.add_event_callback(11, f2)

GPIO.setup(11, GPIO.OUT)
