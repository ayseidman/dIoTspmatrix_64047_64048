from MatrixSparseDOK import MatrixSparseDOK
from MessageHandler import MessageHandler
from Sensor import Sensor
from Time import now, Time
from Logger import Logger, LogNotFoundError
from machine import Timer
from TFT import TFT


class SparseMatrixProcessingEngine:
    TIMER_PERIOD = 10000 # Check in each minute
    # Simulation run longer than real.

    def __init__(self, message_handler=MessageHandler, sensor=Sensor, logger=Logger, screen=TFT):
        self._log_today = MatrixSparseDOK()
        self._logger_enable = True
        self._matrix_manipulated = False

        if not callable(message_handler):
            raise ValueError("Message Handler Class must be callable.")

        if not callable(sensor):
            raise ValueError("Sensor Class must be callable.")

        if not callable(sensor):
            self._logger_enable = False

        self._message_handler = message_handler(matrix_engine=self)
        self._sensor = sensor(callback=self._sensor_callback)
        self._logger = logger()
        self._screen = screen()
        self.initialize()

        self._last_checked_time = now()
        self._timer = Timer(0)
        self._timer.init(period=SparseMatrixProcessingEngine.TIMER_PERIOD, mode=Timer.PERIODIC, callback=self._check_new_day)

    def initialize(self):
        self._message_handler.initialize()

    def run(self):
        self._message_handler.run()

    def read_one_day(self, day_offset):
        requested_date = SparseMatrixProcessingEngine.convert_day_offset_to_date(day_offset)
        try:
            log = self._logger.read(requested_date)

            if log.compressed:
                return MatrixSparseDOK.decompress(log.compressed_matrix)
            else:
                return log.matrix

        except LogNotFoundError:
            # Matrix is not in logs. Return Empty Matrix
            return MatrixSparseDOK()
        

    def read_one_hour(self, day_offset, hour):
        requested_matrix = self.read_one_day(day_offset)
        return requested_matrix.row(hour)

    def read_one_minute(self, day_offset, minute):
        requested_matrix = self.read_one_day(day_offset)
        return requested_matrix.col(minute)

    @staticmethod
    def convert_day_offset_to_date(day_offset: int) -> Time:
        if not isinstance(day_offset, int):
            raise ValueError("Wrong Day Format!")

        present_time = now()
        if day_offset > 0:
            raise ValueError("There is no future data. (System is causal)")

        return present_time+day_offset

    def _sensor_callback(self):
        """ Log into MatrixSparseDOK object by looking current time. """
        present_time = now()
        self._log_today[present_time.hour, present_time.minute] += 1
        print(self._log_today)
        self._matrix_manipulated = True
        

    def _check_new_day(self, value=None):
        """ Check if it is a new day. If so, insert yesterday's log in logger.
            Also regularly draw matrix to the screen, if matrix is change.
        """
        print("Check if it is new day!")

        if self._matrix_manipulated:
            # Matrix is manipulated draw new matrix
            self._screen.print_matrix(self._log_today)
            self._matrix_manipulated = False

        present_time = now()
        if self._last_checked_time.day != present_time.day:
            """ New Day. Write logs and clear matrix"""
            print("New Day!")
            if self._logger_enable:
                self._logger.insert(self._log_today)

            del self._log_today
            self._log_today = MatrixSparseDOK()
            self._screen.clear()

            print("Logging is done!")

        self._last_checked_time = present_time


