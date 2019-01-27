"""Radiator Class."""

from tkinter import StringVar, Frame
from subsystems.Subsystem import Subsystem
from widgets.QuantityVar import QuantityVar


class Radiator(Subsystem):
    """Contains Radiator Data."""

    def __init__(self, data, type):
        """Init the Radiator."""
        self.data = data
        self.radiators = data.radiators
        self.radiator_data = data.radiators[type]
        self.radiators_type = StringVar(value=type)
        self.mass = QuantityVar(unit="g")
        self.area = QuantityVar(unit="m²")
        self.waste_heat = QuantityVar(unit="W")
        self.radiator_temperature = QuantityVar(unit="K")

    def make_entry(self, frame):
        """Creates the Entry for Radiator Stuff."""
        entry = {
            "Radiator": {
                "value": self.radiators_type,
                "unit": "",
                "type": "Combobox",
                "list": [key for key in self.radiators]
            }
        }
        self._make_entry(frame, "Auxiliary Thruster", entry)

    def make_display(self, frame=None):
        """Creates the Display for the Radiator Stuff."""
        data = {
            "Radiator Type": {
                "value": self.radiators_type,
            },
            "Radiator Temperature": {
                "value": self.radiator_temperature,
            },
            "Waste Heat": {
                "value": self.waste_heat,
            },
            "Area": {
                "value": self.area,
            },
            "Mass": {
                "value": self.mass,
            }
        }
        self._make_display(frame, "Radiators", data)

    def calculate(self, waste_heat=0):
        """Calculates the Radiator Data."""
        radiator_type = self.radiators_type.get()
        data = self.radiators[radiator_type]
        if not waste_heat:
            for _, subsystem in self.data.wasteheat.items():
                waste_heat += subsystem
        self.waste_heat.set(waste_heat)
        area = waste_heat / (data["Specific area heat"] * 1000)
        mass = (area * 1000) * data["Specific area mass"]
        self.data.masses["Lifesupport Radiators"] = mass
        self.area.set(area)
        self.mass.set(mass)
        self.radiator_temperature.set(self.radiators[radiator_type]["Radiator Temperature"])

    def make_tab(self, root):
        """Creates a Tab Widgets with the Entry and Data Displays.

        Makes use of self.make_entry and self.make_display.
        """
        self.frame = Frame(root)
        self.make_entry(self.frame)
        self.make_display(self.frame)
        return self.frame
