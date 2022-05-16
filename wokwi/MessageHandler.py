from MQTT import MQTT
from ujson import dumps, loads
from Message import Message, MessageDestinationError
from CommandMessage import CommandMessage
from DataMessage import DataMessage
from NetworkMessage import NetworkMessage


class MessageHandler:

    def __init__(self, communication_interface=MQTT):
        Message.CLIENT_ID = MQTT.CLIENT_ID # Sharing CLIENT_ID with all message types
        self._communication_interface = communication_interface()
        self._communication_interface.set_callback(self._cmd_receive, self._data_receive, self._net_receive)

    def run(self):
        self._communication_interface.connect()

    def stop(self):
        self._communication_interface.disconnect()

    def _cmd_receive(self, message_str):
        """ Handle messages coming from CMD topic. """
        try:
            message = CommandMessage(message_str)
        except MessageDestinationError:
            # Do nothing, wrong node
            return None

    def _data_receive(self, message_str):
        """ Handle messages coming from DATA topic. """
        try:
            message = DataMessage(message_str)
        except MessageDestinationError:
            # Do nothing, wrong node
            return None

    def _net_receive(self, message_str):
        """ Handle messages coming from NET topic. """
        try:
            message = NetworkMessage(message_str)
        except MessageDestinationError:
            # Do nothing, wrong node
            return None


