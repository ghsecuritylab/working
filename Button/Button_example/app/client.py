#!/usr/bin/python
import RPi.GPIO as GPIO
import time

import os
import argparse

import six

import txaio
txaio.use_twisted()

import RPi.GPIO as GPIO

from twisted.internet import reactor
from twisted.internet.defer import inlineCallbacks
from twisted.internet.error import ReactorNotRunning

from autobahn.util import utcnow
from autobahn.twisted.util import sleep
from autobahn.twisted.wamp import ApplicationSession, ApplicationRunner
from autobahn.wamp.exception import ApplicationError



# if GPIO.event_detected(channel):
#     print('Button pressed')

def get_serial():
    """
    Get the Pi's serial number.
    """
    with open('/proc/cpuinfo') as fd:
        for line in fd.read().splitlines():
            line = line.strip()
            if line.startswith('Serial'):
                _, serial = line.split(':')
                return serial.strip().lstrip('0')


def config_button_gpio(channel):

    # Pinreferenz waehlen
    GPIO.setmode(GPIO.BCM)

    # GPIO 18 (Pin 12) als Input definieren und Pullup-Widerstand aktivieren
    GPIO.setup(channel, GPIO.IN, pull_up_down = GPIO.PUD_UP)

    #    # add rising edge detection on a channel

def config_LED_gpio(LED_pin):

    # Pinreferenz waehlen
    GPIO.setmode(GPIO.BCM)

    # GPIO 18 (Pin 12) als Input definieren und Pullup-Widerstand aktivieren
    GPIO.setup(LED_pin, GPIO.OUT)

    #    # add rising edge detection on a channel

class ButtonComponent(ApplicationSession):
    """Our component wrapping a Button interrupt."""

    LED_status = False
    @inlineCallbacks
    def onJoin(self, details):
        LED_pin = 15

        self.LED_status = False
        """Callback when the WAMP session has been established and is ready for use."""
        # get the Pi serial number
        self._serial = get_serial()

        # all procedures/events will have this URI prefix
        self._prefix = u'io.crossbar.demo.iotstarterkit.{}.button'.format(self._serial)

        # print startup infos
        self.log.info("Crossbar.io IoT Starterkit Serial No.: {serial}", serial=self._serial)
        self.log.info("ButtonComponent connected: {details}", details=details)

        # get component user extra configuration
        cfg = self.config.extra

        # initialize button
        self._button_pin = cfg['button_pin']
        GPIO.setwarnings(False)
        # config_button_gpio(_button_pin)
        config_button_gpio(18)
        GPIO.add_event_detect(18, GPIO.FALLING, callback = self.press, bouncetime = 250)


        #initialize LED
        config_LED_gpio(LED_pin)

        # remember startup timestamp
        self._started = utcnow()

        # flag indicating if the button is already pressed
        self._is_pressed = False

        # register procedures
        for proc in [
            (self.started, u'started'),
            (self._is_pressed, u'is_pressed'),
            (self.press, u'press'),
            (self.led_on,u'led_on'),
            (self.led_off,u'led_off')
        ]:
            uri = u'{}.{}'.format(self._prefix, proc[1])
            yield self.register(proc[0], uri)
            self.log.info('registered procedure {uri}', uri=uri)

        self._is_ready = True
        self.log.info("ButtonComponent ready!")

    def started(self):
        """
        Get UTC timestamp when the component started.

        :returns: ISO8601 formatted UTC timestamp when the component started.
        :rtype: str
        """
        return self._started

    def is_pressed(self):
        """
        Check if the buzzer is currently playing a beeping sequence, and hence a (further)
        concurrent call to beep() will fail.

        :returns: Flag indicating whether the buzzer is currently beeping.
        :rtype: bool
        """
        return self._is_pressed

    def get_status(self):
        return self.LED_status


    def set_status(self,status):

        self.LED_status = status
        # self.log.info(self.get_status())
        return 0

    @inlineCallbacks
    def press(self,portnr=1000):
        """Trigger button press."""

        if self._is_pressed:
            raise ApplicationError(u'{}.already-pressed'.format(self._prefix), 'Button is already pressed ')

        self._is_pressed = True
        self.log.info("Pressed")

        self.publish(u'{}.button_pressed'.format(self._prefix))
        yield sleep(1000 / 1000.)
        self._is_pressed = False
        self.publish(u'{}.button_released'.format(self._prefix))
        self.log.info("released")

    @inlineCallbacks
    def led_on(self,LED_pin=15):
        if self.get_status()==False:
            GPIO.output(LED_pin, GPIO.HIGH)
            self.publish(u'{}.LED_on'.format(self._prefix))
            self.log.info("LED_on")
            self.set_status(True)
            pass
        yield sleep(1 / 1000.)

    @inlineCallbacks
    def led_off(self,LED_pin=15):
        if self.get_status()==True:
            GPIO.output(LED_pin, GPIO.LOW)
            self.publish(u'{}.LED_off'.format(self._prefix))
            self.log.info("LED_off")
            self.set_status(False)
            pass
        yield sleep(1 / 1000.)


    @inlineCallbacks
    def onLeave(self, details):
        self.log.info("session closed: {details}", details=details)
        self.disconnect()
        GPIO.output(15, GPIO.LOW)
        GPIO.cleanup()

    def onDisconnect(self):
        self.log.info("connection closed")
        try:
            reactor.stop()
        except ReactorNotRunning:
            pass



if __name__ == '__main__':

    # Crossbar.io connection configuration
    url = os.environ.get('CBURL', u'wss://demo.crossbar.io/ws')
    realm = os.environ.get('CBREALM', u'crossbardemo')

    # parse command line parameters
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--debug', action='store_true', help='Enable debug output.')
    parser.add_argument('--url', dest='url', type=six.text_type, default=url, help='The router URL (default: "ws://localhost:8080/ws").')
    parser.add_argument('--realm', dest='realm', type=six.text_type, default=realm, help='The realm to join (default: "realm1").')

    args = parser.parse_args()

    if args.debug:
        txaio.start_logging(level='debug')
    else:
        txaio.start_logging(level='info')

    # custom configuration data
    extra = {
        # GPI pin of buzzer
        u'button_pin': 18,
    }


    # create and start app runner for our app component ..
    runner = ApplicationRunner(url=args.url, realm=args.realm, extra=extra)
    runner.run(ButtonComponent, auto_reconnect=True)
