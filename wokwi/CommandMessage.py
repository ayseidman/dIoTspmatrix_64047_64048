from Message import Message, MessageDestinationError


class CommandMessage(Message):

    def __init__(self, message=None, cmd=None, day=0, hour=0, minute=0, destination_node_id=None, source_node_id=Message.CLIENT_ID, message_id=None):
        super().__init__(message)
        self._cmd = None
        self._day = None
        self._hour = None
        self._minute = None
        self._destination_node_id = None

        self._message_id = None
        if message is not None:
            self._parse()
        else:
            self._serialize(cmd, day, hour, minute, destination_node_id, source_node_id, message_id)

    def _parse(self):
        self._validate()
        self.cmd = self.body["cmd"]
        self.day = self.body["day"]

        self.destination_node_id = self.body["node_to"]
        self.message_id = self.body["msg_id"]

    def _serialize(self, cmd, day, hour, minute, destination_node_id, source_node_id, message_id):
        if hour is not None:
            self.hour = hour
            self.body["hour"] = hour

        if minute is not None:
            self.minute = minute
            self.body["minute"] = minute

        self.cmd = cmd
        self.body["cmd"] = cmd

        self.day = day
        self.body["day"] = day

        try:
            self.destination_node_id = destination_node_id
        except MessageDestinationError:
            self._destination_node_id = destination_node_id

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
        hour_found = "hour" in self.body
        minute_found = "minute" in self.body

        if value == "GET-NODE-LOG-FULL":
            pass
        elif value == "GET-NODE-LOG-BY-HOUR" and hour_found:
            self.hour = self.body["hour"]
        elif value == "GET-NODE-LOG-BY-MINUTE" and minute_found:
            self.minute = self.body["minute"]
        elif value == "GET-ALL-LOG-FULL":
            pass
        else:
            raise ValueError("Wrong Command Format!")

        self._cmd = value

    @property
    def day(self) -> int:
        return self._day

    @day.setter
    def day(self, value: int):
        if not isinstance(value, int):
            raise ValueError("Wrong Day Format!")

        if value > 0:
            raise ValueError("Wrong Day Format!")
        self._day = value

    @property
    def hour(self) -> int:
        return self._hour

    @hour.setter
    def hour(self, value: int):
        if not isinstance(value, int):
            raise ValueError("Wrong Hour Format!")

        if value < 0 or value > 23:
            raise ValueError("Wrong Hour Format!")

        self._hour = value

    @property
    def minute(self) -> int:
        return self._minute

    @minute.setter
    def minute(self, value: int):
        if not isinstance(value, int):
            raise ValueError("Wrong Hour Format!")

        if value < 0 or value > 59:
            raise ValueError("Wrong Minute Format!")

        self._minute = value

    @property
    def destination_node_id(self) -> str:
        return self._destination_node_id

    @destination_node_id.setter
    def destination_node_id(self, value: str):
        if not isinstance(value,str):
            ValueError("Wrong Command Format!")

        if value not in ["ANY", Message.CLIENT_ID]:
            raise MessageDestinationError()
        self._destination_node_id = value

    def _validate(self):
        keys = ["day", "node_from", "node_to", "msg_id"]
        if not all(key in self.body for key in keys):
            raise ValueError("Wrong Command Format!")
