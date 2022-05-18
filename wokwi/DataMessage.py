from Message import Message, MessageDestinationError
from MQTT import MQTT
from LogTime import LogTime


class DataMessage(Message):

    def __init__(self, message=None, cmd=None, data=[], log_time=None, destination_node_id=None, source_node_id=None, message_id=None):
        super().__init__(message)
        self._cmd = None
        self._data = None
        self._log_time = None
        self._destination_node_id = None
        self._source_node_id = None
        self._message_id = None

        if message is not None:
            self._parse()
        else:
            self._serialize(cmd, data, log_time, destination_node_id, source_node_id, message_id)

    def _parse(self):
        self._validate()
        self.cmd = self.body["cmd"]
        self.data = self.body["data"]
        self.log_time = self.body["log_time"]
        self.destination_node_id = self.body["node_to"]
        self.message_id = self.body["msg_id"]

    def _serialize(self, cmd, data, log_time, destination_node_id, source_node_id, message_id):
        self.cmd = cmd
        self.body["cmd"] = cmd

        self.data = data
        self.body["data"] = data

        self.log_time = log_time
        self.body["log_time"] = str(log_time)

        self.destination_node_id = destination_node_id
        self.body["node_to"] = destination_node_id

        self.source_node_id = source_node_id
        self.body["node_from"] = source_node_id

        self.message_id = message_id
        self.body["msg_id"] = message_id

    @property
    def cmd(self) -> str:
        return self._cmd

    @cmd.setter
    def cmd(self, value: str):
        if not isinstance(value, str):
            raise ValueError("Wrong Command Format!")

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

        self._cmd = value

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value: str):
        if not isinstance(value,list):
            raise ValueError("Wrong Data Format!")

        self._data = value

    @property
    def log_time(self) -> LogTime:
        return self._log_time

    @log_time.setter
    def log_time(self, value: (str, LogTime)):
        if isinstance(value, LogTime):
            self._log_time = value
        else:
            self._log_time = LogTime(value)

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
