from MatrixSparseDOK import MatrixSparseDOK
from Time import now, Time


class LogNotFoundError(Exception):

    def __init__(self, date: Time):
        super().__init__("Log instance for date {}/{}/{} cannot be found.".format(date.day,date.month,date.year))


class LogItem:

    def __init__(self, compressed_matrix, log_time, compressed=True):
        if compressed:
            self.compressed_matrix = compressed_matrix
        else:
            self.matrix = compressed_matrix
        self.log_time = log_time
        self.compressed = compressed

    @property
    def matrix(self):
        return self._matrix

    @matrix.setter
    def matrix(self, value):
        if not isinstance(value, MatrixSparseDOK):
            raise ValueError("Wrong Matrix Format")

        self._matrix = value

    @property
    def compressed_matrix(self):
        return self._compressed_matrix

    @compressed_matrix.setter
    def compressed_matrix(self, value):
        if not isinstance(value, tuple):
            raise ValueError("Wrong Compressed Matrix")

        if len(value) != 5:
            raise ValueError("Wrong Compressed Matrix")

        self._compressed_matrix = value

    @property
    def log_time(self):
        return self._log_time

    @log_time.setter
    def log_time(self, time):
        if not isinstance(time, Time):
            raise ValueError("Wrong Time Format")

        self._log_time = time


class Logger:

    def __init__(self):
        self._logs = {}

    def insert(self, matrix: MatrixSparseDOK):
        compressed_flag = True
        try:
            compressed = matrix.compress()
        except ValueError as err:
            if str(err) == "compress() dense matrix":
                # IF matrix is dense, insert itself instead of compressing
                compressed = matrix
                compressed_flag = False
                

        log_time = now()
        log = LogItem(compressed, log_time, compressed=compressed_flag)
        # Insert the new log!
        date_tuple = (log_time.year, log_time.month, log_time.day)
        self._logs[date_tuple] = log

    def read(self, date: Time) -> LogItem:
        if not isinstance(date, Time):
            raise ValueError("Wrong Date Format!")
        date_tuple = (date.year, date.month, date.day)
        if date_tuple not in self._logs:
            raise LogNotFoundError(date)

        return self._logs[date_tuple]

    def clear(self, date: Time):
        if not isinstance(date, Time):
            raise ValueError("Wrong Date Format!")

        if date not in self._logs:
            raise LogNotFoundError(date)

        del self._logs[date]

    def export_log(self):
        pass

    def import_log(self):
        pass

