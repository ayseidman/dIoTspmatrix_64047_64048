class LogTime:

    def __init__(self, time_string):
        self._time = None
        self._hour = None
        self._minute = None

    @property
    def time(self):
        raise NotImplementedError("There is no getter for time")

    @time.setter
    def time(self):
        pass

    def __str__(self):
        return f"{self._hour}:{self._minute}"
