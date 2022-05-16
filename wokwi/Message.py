from ujson import loads, dumps


class MessageDestinationError(Exception):
    """ Message Destination is not current Node! """
    def __init__(self):
        super().__init__("Wrong Message Destination")


class Message:

    CLIENT_ID = None

    def __init__(self, message):
        self.body = message

    @property
    def body(self) -> dict:
        """ Python getter for zero """
        return self._body

    @body.setter
    def body(self, message: str):
        """ Validate the common keys of messages from all topics"""
        if not isinstance(message, str):
            raise ValueError("Wrong Message Format!")

        message_json = Message._parse_json(message)

        if "cmd" not in message_json:
            raise ValueError("Wrong Message Format!")

        self._body = message_json

    @staticmethod
    def _parse_json(message: str) -> dict:
        """ Parsing JSON messages coming from interface. """
        json_dict = loads(message)
        return json_dict

