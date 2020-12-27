from spidev import SpiDev

from enum import Enum


class Bus(Enum):
    SPI0 = 0
    SPI1 = 1

class Device(Enum):
    CE0 = 0
    CE1 = 1

class SPIDevice:

    @staticmethod
    def _get_mode(
        polarity,
        phase
    ):
        if polarity == 0: 
            if phase == 0:
                return 0
            else:
               return 1
        else:
            if phase == 0:
                return 2
            else:
               return 3


    def __init__(
        self,
        bus,
        device,
        baudrate=1000000,
        polarity=0,
        phase=0
    ):
        self._spi = SpiDev()
        self._bus = bus
        self._device = device
        self._spi_baudrate = baudrate
        self._spi_mode = self._get_mode(polarity,phase)
        self._open = False

    def open(self):
        self._spi.open(self._bus, self._device)
        self._spi.max_speed_hz = self._spi_baudrate
        self._spi.mode = self._spi_mode
        self._open = True

    def write_read(self, data):
        if not self._open:
            self.open()
        in_buf = self._spi.xfer(data)
        return in_buf

    def write(self, data):
        if not self._open:
            self.open()
        self._spi.writebytes(data)

    def close(self):
        self._spi.close()
        self._open = False
