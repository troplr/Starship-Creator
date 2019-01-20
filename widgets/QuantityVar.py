"""Variable Class for QuantiPhy Quantity."""

from tkinter import StringVar
from quantiphy import Quantity, UnitConversion

tonne = UnitConversion('g', 't tonne', 1e6)
watt = UnitConversion('W', 'W Watt')


class QuantityVar(StringVar):
    """Variable Class for QuantiPhy Quantity."""

    def __init__(self, master=None, value=None, name=None, unit='g'):
        """Construct a Quantity variable.

        MASTER can be given as master widget.
        VALUE is an optional value (defaults to "")
        NAME is an optional Tcl name (defaults to PY_VARnum).
        If NAME matches an existing variable and VALUE is omitted
        then the existing value is retained.
        UNIT sets the Unit of the Quantity variable
        """
        StringVar.__init__(self, master, value, name)
        self.unit = unit

    def set(self, value, unit=None):
        """Sets the Quantity Variable."""
        if not unit:
            unit = self.unit
        if unit == 'kg' and value > 1000:
            unit = 't'
            value = value / 1000
        if unit == 'g' and value > 1e6:
            unit = 't'
            value = value / 1e6
        self.quantity = Quantity(value, unit)
        if unit == "m³" or unit == "m²":
            string = '{:p}'.format(self.quantity)
        else:
            string = '{}'.format(self.quantity)
        StringVar.set(self, value=string)

    def get(self, unit=None):
        """Returns the Real value of the Quantity Variable."""
        if not unit:
            unit = self.unit
        value = self.quantity.real
        return value
