from MatrixSparseDOK import MatrixSparseDOK
from Time import now, Time
from machine import SDCard
from os import mount, mkdir, listdir, chdir


class LogNotFoundError(Exception):

    def __init__(self, date: Time):
        super().__init__("Log instance for date {}/{}/{} cannot be found.".format(date.day, date.month, date.year))


class LogItem:
    """ MatrixMarket (MM) Format. """

    def __init__(self, matrix=None, log_time=None, mm_str=None):
        if mm_str is None:
            self.matrix = matrix
            self.log_time = log_time
        else:
            self.matrix = LogItem._convert_file_to_logitem(mm_str)
            self.log_time = log_time

    @property
    def matrix(self):
        return self._matrix

    @matrix.setter
    def matrix(self, value):
        if not isinstance(value, MatrixSparseDOK):
            raise ValueError("Wrong Matrix Format")

        self._matrix = value

    @property
    def log_time(self):
        return self._log_time

    @log_time.setter
    def log_time(self, time):
        if not isinstance(time, Time):
            raise ValueError("Wrong Time Format")

        self._log_time = time

    def __str__(self):
        """ Return MatrixMarket (MM) Format String to be written in file.
            #row      #col      #entry
             r(1)      c(1)      val(1)
             r(2)      c(2)      val(2)
             r(3)      c(3)      val(3)
              .         .          .
              .         .          .
              .         .          .
         r(#entry)  c(#entry)  val(#entry)
         See also: https://math.nist.gov/MatrixMarket/formats.html
        """
        min_pos, max_pos = self.matrix.dim()
        num_row = max_pos[0] - min_pos[0] + 1
        num_col = max_pos[1] - min_pos[1] + 1
        MM_format = "{} {} {}\n".format(num_row, num_col, len(self.matrix))

        for entry in self.matrix:
            row, col = entry[0], entry[1]
            value = self.matrix[entry]
            MM_format += "{} {} {:.1f}\n".format(row, col, value)

        return MM_format

    @staticmethod
    def _convert_file_to_logitem(mm_str: str):
        if not isinstance(mm_str, str):
            raise ("Wrong Format for MM String")

        lines = mm_str.splitlines()
        num_row, num_col, num_entry = map(int, lines[0].split())
        entries = lines[1:]
        matrix = MatrixSparseDOK()
        for entry in entries:
            row, col, value = entry.split()
            row = int(row)
            col = int(col)
            value = float(value)
            matrix[row, col] = value

        return matrix


class Logger:
    DEFAULT_SPI_SCK = 18
    DEFAULT_SPI_MOSI = 23
    DEFAULT_SPI_MISO = 19
    DEFAULT_SPI_CS = 5
    DEFAULT_SPI_CD = 34

    def __init__(self):
        self._logs = {}
        self._main_directory = "/logs"
        # Connect SD Card
        self._sd_card = SDCard(slot=2, cd=Logger.DEFAULT_SPI_CD, sck=Logger.DEFAULT_SPI_SCK,
                               miso=Logger.DEFAULT_SPI_MISO,
                               mosi=Logger.DEFAULT_SPI_MOSI, cs=Logger.DEFAULT_SPI_CS, freq=40000000)
        mount(self._sd_card, self._main_directory)

    def insert(self, matrix: MatrixSparseDOK):
        """ Insert a log and save as a file """
        log_time = now()
        log = LogItem(matrix, log_time)
        # Insert the new log!
        log_filename = "{:04}_{:02}_{:02}.txt".format(log_time.year, log_time.month, log_time.day)

        with open(log_filename, "w") as log_file:
            log_file.write(str(log))

        # For Test
        with open(log_filename) as log_file:
            print(log_file.read())

    def read(self, date: Time) -> LogItem:
        """ Read requested log """
        if not isinstance(date, Time):
            raise ValueError("Wrong Date Format!")
        log_filename = "{:04}_{:02}_{:02}.txt".format(date.year, date.month, date.day)
        date.hour = 23
        date.minute = 59

        try:
            with open(log_filename) as log_file:
                MM_file = log_file.read()
        except OSError as err:
            raise LogNotFoundError(date)
        requested_log = LogItem(mm_str=MM_file, log_time=date)

        return requested_log

    def clear(self, date: Time):
        # ToDo: Must be checked
        if not isinstance(date, Time):
            raise ValueError("Wrong Date Format!")

        if date not in self._logs:
            raise LogNotFoundError(date)

        del self._logs[date]

    def import_log(self):
        date = now()
        return self.read(date).matrix