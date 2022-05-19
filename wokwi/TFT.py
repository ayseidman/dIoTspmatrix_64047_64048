from machine import Pin, SoftSPI
from ili9341 import ILI9341, color565
from MatrixSparseDOK import MatrixSparseDOK
from sys import maxsize


DEFAULT_SPI_SCK = 18
DEFAULT_SPI_MOSI = 23
DEFAULT_SPI_MISO = 13
DEFAULT_SPI_CS = 15
DEFAULT_SPI_DC = 2
DEFAULT_SPI_CHANNEL = SoftSPI(baudrate=40000000, polarity=1, phase=0, sck=Pin(DEFAULT_SPI_SCK), mosi=Pin(DEFAULT_SPI_MOSI), miso=Pin(DEFAULT_SPI_MISO))


class TFT(ILI9341):

    def __init__(self, spi_channel=DEFAULT_SPI_CHANNEL):
        super().__init__(spi_channel, cs=Pin(DEFAULT_SPI_CS), dc=Pin(DEFAULT_SPI_DC))
        self._width = 240
        self._height = 360
        self._min_value = 0
        self._start_pos = (int((self._width-120)/2),int((self._height-48)/2))
        self._positions = []
        self._print_borders()

    def _print_borders(self):
        self.fill_rectangle(self._start_pos[0]-1, self._start_pos[1]-1, 122, 1, color565(255, 0, 0))
        self.fill_rectangle(self._start_pos[0]-1, self._start_pos[1]-1, 1, 50, color565(255, 0, 0))

        self.fill_rectangle(self._start_pos[0]-1, self._start_pos[1]+48, 122, 1, color565(255, 0, 0))
        self.fill_rectangle(self._start_pos[0]+120, self._start_pos[1]-1, 1, 50, color565(255, 0, 0))

    def print_matrix(self, matrix: MatrixSparseDOK):
        max_value = TFT.find_max(matrix)
        for pos in matrix:
            value = matrix[pos]
            color = int((value-self._min_value)/(max_value-self._min_value)*255)
            y, x = int(pos[0]*2), int(pos[1]*2)
            self._positions.append(pos)
            self.pixel(self._start_pos[0] + x, self._start_pos[1] + y, color565(color, color, color))
            self.pixel(self._start_pos[0] + x, self._start_pos[1] + y+1, color565(color, color, color))
            self.pixel(self._start_pos[0] + x+1, self._start_pos[1] + y, color565(color, color, color))
            self.pixel(self._start_pos[0] + x+1, self._start_pos[1] + y+1, color565(color, color, color))

    @staticmethod
    def find_max(matrix: MatrixSparseDOK):
        max_value = -1
        for pos in matrix:
            value = matrix[pos]
            if value > max_value:
                max_value = value

        return max_value

    def clear(self):
        for pos in self._positions:
            self.pixel(self._start_pos[0]+pos[1]*2, self._start_pos[1]+pos[0]*2, color565(0,0,0))
            self.pixel(self._start_pos[0] + pos[1]*2+1, self._start_pos[1] + pos[0]*2, color565(0, 0, 0))
            self.pixel(self._start_pos[0] + pos[1]*2, self._start_pos[1] + pos[0]*2+1, color565(0, 0, 0))
            self.pixel(self._start_pos[0] + pos[1]*2+1, self._start_pos[1] + pos[0]*2+1, color565(0, 0, 0))

        self._positions.clear()




