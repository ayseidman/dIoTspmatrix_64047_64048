from ujson import loads, dumps


class MessageDestinationError(Exception):
    """ Message Destination is not current Node! """
    def __init__(self):
        super().__init__("Wrong Message Destination")


class Message:

    CLIENT_ID = None

    def __init__(self, message = None):
        self._body = {}
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

        self._body = message_dict

    @staticmethod
    def _parse_json(message: str) -> dict:
        """ Parsing JSON messages coming from interface. """
        message_dict = loads(message)
        return message_dict

    def __str__(self):
        return dumps(self._body)

