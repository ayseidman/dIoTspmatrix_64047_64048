from Message import Message, MessageDestinationError
from MQTT import MQTT
from ast import literal_eval
from LogTime import LogTime

class DataMessage(Message):

    def __init__(self, message):
        super().__init__(message)
        self._type = None
        self._data = None
        self._log_time = None
        self._destination_node_id = None
        self._source_node_id = None
        self._message_id = None

        self._cmd_parse()

    def _cmd_parse(self):
        self._validate()
        self.type = self.body["cmd"]
        self.data = self.body["data"]
        self.log_time = self.body["log_time"]
        self.destination_node_id = self.body["node_to"]
        self.source_node_id = self.body["node_from"]
        self.message_id = self.body["msg_id"]

    @property
    def type(self) -> str:
        return self._type

    @type.setter
    def type(self, value: str):
        if value == "GET-NODE-LOG-FULL":
            pass
        elif value == "GET-NODE-LOG-BY-HOUR":
            pass
        elif value == "GET-NODE-LOG-BY-MINUTE":
            pass
        elif value == "GET-LOG-FULL-EDGE":
            pass
        else:
            raise ValueError("Wrong Command Format!")

        self._type = value

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value: str):
        try:
            value = literal_eval(value)
        except (ValueError, TypeError, SyntaxError, MemoryError, RecursionError):
            raise ValueError("Wrong Data Format!s")

        self._data = value

    @property
    def log_time(self) -> LogTime:
        return self._log_time

    @log_time.setter
    def log_time(self, value: str):
        self._log_time = LogTime(str)

    @property
    def destination_node_id(self) -> str:
        return self._destination_node_id

    @destination_node_id.setter
    def destination_node_id(self, value: str):
        if value not in ["ANY", MQTT.CLIENT_ID]:
            raise MessageDestinationError()
        self._destination_node_id = value

    def _validate(self):
        keys = ["data", "log_time", "node_from", "node_to", "msg_id"]
        if not all(key in self.body for key in keys):
            raise ValueError("Wrong Command Format!")
