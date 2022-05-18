import ntptime
from machine import RTC
from time import localtime

# Time Configs
ntptime.host = "1.europe.pool.ntp.org"
UTC = 1

RTC = RTC()

def now():
    return Time(localtime())

def synchronize_local_time():
    """ Set current time from NTP server. """
    ntptime.settime()
    year, month, day, hour, minute, second, weekday, yearday = localtime()
    # Add UTC
    RTC.datetime((year, month, day, weekday, hour + UTC, minute, second, 0))
    print("Time is set to ", now())

class Time:

    def __init__(self, time=None):
        self.year = None
        self.month = None
        self.day = None
        self.hour = None
        self.minute = None
        self.second = None

        if isinstance(time, str):
            self.str_to_time(time)
        elif isinstance(time, tuple):
            self.tuple_to_time(time)

    def __str__(self):
        return f"{self.year}-{self.month:02}-{self.day:02} {self.hour:02}:{self.minute:02}:{self.second:02}"

    def str_to_time(self, time_str):
        try:
            time_fields = time_str.split(" ")
            date_field = time_fields[0].split("-")
            time_field = time_fields[1].split(":")

            self.year = int(date_field[0])
            self.month = int(date_field[1])
            self.day = int(date_field[2])

            self.hour = int(time_field[0])
            self.minute = int(time_field[1])
            self.second = int(time_field[2])

        except ValueError:
            raise ValueError("Wrong Time  Format!")

    def tuple_to_time(self, time_tuple):
        if not all([isinstance(item, int) for item in time_tuple]):
            raise ValueError("Wrong Network Message Format!")

        self.year = time_tuple[0]
        self.month = time_tuple[1]
        self.day = time_tuple[2]

        self.hour = time_tuple[3]
        self.minute = time_tuple[4]
        self.second = time_tuple[5]
