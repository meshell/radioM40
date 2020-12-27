from mcp3008 import MCP3008


class AnalogIn:
    """AnalogIn Mock Implementation for ADC Reads.
    :param MCP3002,MCP3004,MCP3008 mcp: The mcp object.
    :param int positive_pin: Required pin for single-ended.
    :param int negative_pin: Optional pin for differential reads.
    """

    def __init__(self, mcp, pin):
        if not isinstance(mcp, MCP3008):
            raise ValueError("mcp object is not a sibling of MCP3xxx class.")
        self._mcp = mcp
        self._pin = pin

    @property
    def value(self):
        """Returns the value of an ADC pin as an integer. Due to 10-bit accuracy of the chip, the
        returned values range [0, 65472]."""
        return (
            self._mcp.read_channel( self._pin) << 6
        )

    @property
    def voltage(self):
        """Returns the voltage from the ADC pin as a floating point value. Due to the 10-bit
        accuracy of the chip, returned values range from 0 to (``reference_voltage`` *
        65472 / 65535)"""
        return (self.value * self._mcp.reference_voltage) / 65535