from MatrixSparseDOK import MatrixSparseDOK
from Position import Position
from random import randint
from TFT import TFT
from ili9341 import color565
from time import sleep
from Sensor import Sensor
from Time import now, Time


class HeatMapTFT:
    """ This class can be used to test HeatMap functionality of the system. """
    def __init__(self):
        self._matrix = MatrixSparseDOK()
        self._screen = TFT()

    def random(self):
        """ Calculates Random 200 positions in Matrix"""
        for p in range(200):
            x = randint(0, 23)
            y = randint(0, 59)

            self._matrix[Position(x, y)] = randint(0, 10)

        self._screen.print_matrix(self._matrix)
        sleep(5)
        self._screen.clear()

    def diagonal(self):
        x = range(24)
        y = range(60)

        temp = 0

        for x1, y1 in zip(x,y):
            self._matrix[Position(x1, y1)] = temp
            temp += 1

        self._screen.print_matrix(self._matrix)
        sleep(5)
        self._screen.clear()

    def diagonal(self):
        self._matrix = {(1, 1): 1.1, (1, 2): 1.2, (1, 3): 1.3, (2, 1): 2.1, (10, 30): 26, (23, 59): 50}

        for pos, value in self._matrix:
            self._matrix[pos] = value

        self._screen.print_matrix(self._matrix)
        sleep(5)
        self._screen.clear()

    def clear(self):
        self._screen.clear()


class PIRSensor:

    def __init__(self):
        self._sensor = Sensor(pin=12,callback=self._callback)

    def _callback(self, pin):
        print("Motion Detected!")


class TimeTest:

    def __init__(self):
        self._present_time = now()

        print(self._present_time + 1)
        print(self._present_time - 1)

        print(self._present_time + 30)
        print(self._present_time - 30)

