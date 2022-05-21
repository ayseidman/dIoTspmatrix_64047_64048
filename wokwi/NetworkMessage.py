from Message import Message
from time import localtime
from Time import Time, now


class NetworkMessage(Message):
    TIMESTAMP_FORMAT = "%Y-%m-%d %H:%M:%S"

    def __init__(self, message=None, cmd=None, source_node_id=None, timestamp=None, sending=False):
        super().__init__(message, sending=True)
        self._cmd = None
        self._timestamp = None

        if message is not None:
            self._parse()
        else:
            if timestamp is None:
                timestamp = now()
            self._serialize(cmd, source_node_id, timestamp)

    def _parse(self):
        self._validate()
        self.cmd = self.body["cmd"]
        self.timestamp = self.body["timestamp"]

    def _serialize(self, cmd, source_node_id, timestamp):
        self.cmd = cmd
        self.body["cmd"] = cmd

        self.source_node_id = source_node_id
        self.body["node_from"] = source_node_id

        self.timestamp = timestamp
        self.body["timestamp"] = str(self.timestamp)

    @property
    def cmd(self):
        return self._cmd

    @cmd.setter
    def cmd(self, value):
        if not isinstance(value, str):
            raise ValueError("Wrong Network Message Format!")

        if value == "NODE ALIVE":
            pass
        elif value == "NODE DEAD":
            pass
        else:
            raise ValueError("Wrong Network Message Format!")

        self._cmd = value

    @property
    def timestamp(self):
        return self._timestamp

    @timestamp.setter
    def timestamp(self, value: (Time, str)):
        if isinstance(value, Time):
            self._timestamp = value
        elif isinstance(value, str):
            self._timestamp = Time(value)
        else:
            raise ValueError("Wrong Network Message Format!")

    def _validate(self):
        keys = ["node_from", "timestamp"]
        if not all(key in self.body for key in keys):
            raise ValueError("Wrong Network Message Format!")

