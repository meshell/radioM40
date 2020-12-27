import spi
from spi import SPIDevice

class MCP3008(object):
    def __init__(self, bus=spi.Bus.SPI0, device=spi.Device.CE0, ref_voltage=3.3):
        self._spi = SPIDevice(bus, device)
        self._out = bytearray(3)
        self._out[0] = 0x01
        self._ref_voltage = ref_voltage

    @property
    def reference_voltage(self):
        """Returns the reference voltage. (read-only)"""
        return self._ref_voltage

    def read_channel(self, channel):
        self._out[1] = (8 + channel) << 4
        adc = self._spi.write_read(self._out)
        return ((adc[1] & 0x03) << 8) | adc[2]

    def open(self):
        self._spi.open()

    def close(self):
        self._spi.close()