"""Radiator Class."""

from widgets.MultiDisplay import MultiDisplay
from tkinter import DoubleVar, StringVar
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

    def make_entry(self, frame):
        """Creates the Entry for Radiator Stuff."""
        pass

    def make_display(self, frame=None):
        """Creates the Display for the Radiator Stuff."""
        data = {
            "Radiator Type": {
                "value": self.radiators_type,
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
        if not frame:
            frame = self.data_display
        self.data_display = MultiDisplay(frame, "Life Support Radiators")
        self.data_display.make_display(data)

    def calculate(self, waste_heat):
        """Calculates the Radiator Data."""
        self.waste_heat.set(waste_heat)
        area = waste_heat / (self.radiator_data["Specific area heat"] * 1000)
        mass = (area * 1000) * self.radiator_data["Specific area mass"]
        self.area.set(area)
        self.mass.set(mass)

    def change_radiator(self, type):
        """Change the radiator type."""
        self.radiator_data = self.radiators[type]
        self.radiators_type.set(type)
