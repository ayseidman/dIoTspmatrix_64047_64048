class LogTime:

    def __init__(self, time_string=None, hour=0, minute=0):
        self._time = None
        self._hour = None
        self._minute = None
        if time_string is not None:
            self.time = time_string
        else:
            self.hour = hour
            self.minute = minute

    @property
    def time(self):
        return self.hour, self.minute

    @time.setter
    def time(self, value):
        if not isinstance(value, str):
            raise ValueError("LogTime format error!")

        # Split HH:MM
        splited_str = value.split(":")
        if len(splited_str) != 2:
            raise ValueError("LogTime format error!")

        self.hour = splited_str[0]
        self.minute = splited_str[1]

    @property
    def hour(self):
        return self._hour

    @hour.setter
    def hour(self, value):
        try:
            value_int = int(value)
        except ValueError:
            raise ValueError("LogTime format error!")

        if not (0 <= value_int <= 23):
            raise ValueError("LogTime format error!")

        self._hour = value_int

    @property
    def minute(self):
        return self._minute

    @minute.setter
    def minute(self, value):
        try:
            value_int = int(value)
        except ValueError:
            raise ValueError("LogTime format error!")

        if not (0 <= value_int <= 59):
            raise ValueError("LogTime format error!")

        self._minute = value_int

    def __str__(self):
        return f"{self.hour:02}:{self.minute:02}"
