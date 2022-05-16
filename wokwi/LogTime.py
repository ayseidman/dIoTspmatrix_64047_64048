class LogTime:

    def __init__(self, time_string):
        self._time = None
        self.hour = None
        self.minute = None
        self.time = time_string

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

        hour = splited_str[0]
        minute = splited_str[1]

        if not (hour.isnumeric() and minute.isnumeric()):
            raise ValueError("LogTime format error!")
        hour = int(hour)
        minute = int(minute)

        if not (0 <= hour <= 23 and 0 <= minute <= 59):
            raise ValueError("LogTime format error!")

        self.hour = hour
        self.minute = minute

    def __str__(self):
        return f"{self.hour}:{self.minute}"
