from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
from MatrixSparseDOK import MatrixSparseDOK


DEFAULT_I2C_SCL = 22
DEFAULT_I2C_SDA = 21
DEFAULT_I2C_CHANNEL = I2C(0, scl=Pin(DEFAULT_I2C_SCL), sda=Pin(DEFAULT_I2C_SDA))


class OLED(SSD1306_I2C):

    def __init__(self, width=128, height=64, i2c_channel=DEFAULT_I2C_CHANNEL):
        self.width = width
        self.height = height

        super().__init__(width, height, i2c_channel)

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, value):
        OLED._check_dimension(value)

        self._width = value

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, value):
        OLED._check_dimension(value)

        self._height = value

    def print_matrix(self, matrix: MatrixSparseDOK):
        pass

    @staticmethod
    def _check_dimension(value):
        if not isinstance(value, int):
            raise ValueError("Screen dimensions must be integer")

        if value < 0:
            raise ValueError("Screen dimensions must be greater than Zero")






