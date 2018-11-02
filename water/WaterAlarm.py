#!/usr/bin/env python
#
# Authors: Jorge Ramirez Ortiz, Yipeng Sun
# Last Change: Wed Aug 15, 2018 at 06:09 PM -0400


import RPi.GPIO as GPIO
import sys, time

from threading import Thread, Event


class WaterAlarm(Thread):
    def __init__(self, stop_event, *args,
                 ch=9, interval=0.01, alarm_threshold=2, **kwargs):
        self.stop_event = stop_event
        self.ch = ch
        self.interval = interval
        self.alarm_threshold = alarm_threshold

        # 'leak_counter' variable can be used to guard against false alarms.
        #
        # This class will monitor the input pin for a HIGH. It is default LOW
        # due to an internal pulldown resistor. It will probe every 0.1 seconds,
        # and if it detects a leak, then the 'leak_counter' variable will
        # increase by one.
        #
        # It seems as if 1 hit to leak_counter can be safely ignored, even tiny
        # drops that run across the sensor trigger the sensor at least twice.
        #
        # Anything more than 5 hits is a major leak (the sensor is in a puddle
        # of water)
        self.leak_counter = 0

        GPIO.setmode(GPIO.BOARD)

        # nominal: no water means circuit is open & BCM 17 is LOW due to
        #          PULLDOWN
        # water detected: leak sensor closes, becomes 2M ohm resistor & BCM 17
        #                 is HIGH
        GPIO.setup(self.ch, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # activate pin

        super().__init__(*args, **kwargs)

    def cleanup(self):
        GPIO.cleanup(self.ch)
        self.join()

    def read_channel(self):
        return GPIO.input(self.ch)

if __name__ == '__main__':  # ensure that script is being run from terminal
    stop_event = Event()

    print('Initializing water leak detector...')
    alarm = WaterAlarm(stop_event, ch=int(sys.argv[1]))
    alarm.start()
leak = 0 #Starts the counter

#Following if loop establishes initial boolean
if self.read_channel() != 1: #This indicates that the circuit is shorted, therefore there is a leak
    dry = true 
    print('Everything is fine')
else:
    dry=false
    print('Everything is not fine')

while True: #Establishes infinite loop
    if dry == true and self.read_channel()==1:
        leak+=1
        dry = false
        print ('leak #%d has started ' %leak)
        time.sleep(2) #sleeps for two seconds
    elif dry == false and self.read_channel!=1:
        dry = true
        print(' leak #%d has ended' %leak)
        time.sleep(2)
    else:
        time.sleep(5)
    try:
        while True:
            pass
    except KeyboardInterrupt:
        print('Preparing for graceful shutdown...')

    stop_event.set()
    alarm.cleanup()
