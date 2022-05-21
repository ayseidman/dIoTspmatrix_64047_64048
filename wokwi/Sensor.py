from machine import Pin

DEFAULT_PIN = 12


class Sensor:

    def __init__(self, pin=DEFAULT_PIN, rising_edge=True, falling_edge=False,callback=None):
        self._pin = Pin(pin, Pin.IN)
        self._rising_edge = rising_edge
        self._falling_edge = falling_edge
        self._callback_route = callback
        self._interrupt_config()

    def _interrupt_config(self):
        if not (self._rising_edge or self._falling_edge):
            raise ValueError("At least one edge is needed to be presented.")

        if not callable(self._callback_route):
            raise ValueError("Callback function must be callable")
        trigger = Pin.IRQ_RISING if self._rising_edge else 0
        trigger |= Pin.IRQ_FALLING if self._falling_edge else 0
        self._pin.irq(trigger=trigger, handler=self._callback)

    def _callback(self, _):
        self._callback_route()
