from MQTT import MQTT
from Message import Message, MessageDestinationError
from CommandMessage import CommandMessage
from DataMessage import DataMessage
from NetworkMessage import NetworkMessage
from machine import Timer, Pin


class MessageHandler:
    LED_PIN = 13
    TIMER_PERIOD = 10000
    # In simulator, It gives 20 seconds, but in reality it gives 47 seconds period.
    # If timer period pass 60s in reailty, then MQTT server kickouts our node.
    # So that we had to set timer 20 seconds in simulation.

    def __init__(self, communication_protocol=MQTT):
        Message.CLIENT_ID = communication_protocol.CLIENT_ID # Sharing CLIENT_ID with all message types
        self._communication_protocol = communication_protocol()
        self._communication_protocol.set_callback(self._cmd_receive, self._data_receive, self._net_receive)
        self._timer = Timer(3)
        self._led = Pin(MessageHandler.LED_PIN,Pin.OUT)
        self._led_state = 0

    def run(self):
        print("Start")
        self._communication_protocol.connect()
        self._send_alive()
        self._timer.init(period=10000, callback=self._send_alive)
        self._communication_protocol.run()
        

    def stop(self):
        self._communication_protocol.disconnect()

    def _cmd_receive(self, message_str):
        """ Handle messages coming from CMD topic. """
        try:
            message = CommandMessage(message_str)
        except MessageDestinationError:
            # Do nothing, wrong node
            return None
        except ValueError as err:
            print(err)

    def _data_receive(self, message_str):
        """ Handle messages coming from DATA topic. """
        try:
            message = DataMessage(message_str)
        except MessageDestinationError:
            # Do nothing, wrong node
            return None
        except ValueError as err:
            print(err)

    def _net_receive(self, message_str):
        """ Handle messages coming from NET topic. """
        try:
            message = NetworkMessage(message_str)
        except MessageDestinationError:
            # Do nothing, wrong node
            return None
        except ValueError as err:
            print(err)

    def _send_alive(self, value=None):
        print("ALIVE: ")
        self._led_state = 0 if self._led_state else 1
        self._led.value(self._led_state)
        msg = NetworkMessage(None, "NODE ALIVE", self._communication_protocol.CLIENT_ID)
        self._communication_protocol.send_network_info(str(msg))

