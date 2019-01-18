"""Radiator Class."""

from widgets.MultiDisplay import MultiDisplay
from tkinter import DoubleVar, StringVar
from subsystems.Subsystem import Subsystem


class Radiator(Subsystem):
    """Contains Radiator Data."""

    def __init__(self, data, type):
        """Init the Radiator."""
        self.data = data
        self.radiators = data.radiators
        self.radiator_data = data.radiators[type]
        self.radiators_type = StringVar(value=type)
        self.mass = DoubleVar()
        self.area = DoubleVar()
        self.waste_heat = DoubleVar()

    def make_entry(self, frame):
        """Creates the Entry for Radiator Stuff."""
        pass

    def make_display(self, frame=None):
        """Creates the Display for the Radiator Stuff."""
        data = {
            "Radiator Type": {
                "value": self.radiators_type,
                "unit": ""
            },
            "Waste Heat": {
                "value": self.waste_heat,
                "unit": "kW"
            },
            "Area": {
                "value": self.area,
                "unit": "m²"
            },
            "Mass": {
                "value": self.mass,
                "unit": "kg"
            }
        }
        if not frame:
            frame = self.data_display
        self.data_display = MultiDisplay(frame, "Life Support Radiators")
        self.data_display.make_display(data)

    def calculate(self, waste_heat):
        """Calculates the Radiator Data."""
        self.waste_heat.set(waste_heat / 1e3)
        area = waste_heat / self.radiator_data["Specific area heat"]
        mass = waste_heat / self.radiator_data["Specific area mass"]
        self.area.set(area)
        self.mass.set(mass)

    def change_radiator(self, type):
        """Change the radiator type."""
        self.radiator_data = self.radiators[type]
        self.radiators_type.set(type)
