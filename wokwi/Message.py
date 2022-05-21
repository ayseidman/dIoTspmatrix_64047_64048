from ujson import loads, dumps


class MessageDestinationError(Exception):
    """ Message Destination is not current Node! """
    def __init__(self):
        super().__init__("Wrong Message Destination")


class MessageEchoError(Exception):
    """ Message Destination is not current Node! """
    def __init__(self):
        super().__init__("Echo message. Ignore it!")



class Message:

    CLIENT_ID = None

    def __init__(self, message = None, sending=False):
        self._source_node_id = None
        self._body = {}
        self._sending=sending

        if message is not None:
            self.body = message


    @property
    def body(self) -> dict:
        """ Python getter for body """
        return self._body

    @body.setter
    def body(self, message: str):
        """ Validate the common keys of messages from all topics"""
        if not isinstance(message, str):
            raise ValueError("Wrong Message Format!")

        message_dict = Message._parse_json(message)

        if "cmd" not in message_dict:
            raise ValueError("Wrong Message Format!")

        if "node_from" not in message_dict:
            raise ValueError("Wrong Message Format!")

        self.source_node_id = message_dict["node_from"]
        self._body = message_dict

    @property
    def source_node_id(self) -> str:
        return self._source_node_id

    @source_node_id.setter
    def source_node_id(self, value: str):
        if not isinstance(value, str):
            raise ValueError("Wrong Message Format!")

        if value == Message.CLIENT_ID and not self._sending:
            raise MessageEchoError

        self._source_node_id = value

    @staticmethod
    def _parse_json(message: str) -> dict:
        """ Parsing JSON messages coming from interface. """
        message_dict = loads(message)
        return message_dict

    def __str__(self):
        return dumps(self._body)

