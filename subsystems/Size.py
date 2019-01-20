"""Calculates the Volume of the Spacecraft."""

from tkinter import DoubleVar
from subsystems.Subsystem import Subsystem
from widgets.QuantityVar import QuantityVar


class Size(Subsystem):
    """Calculates the Volume of the Spacecraft."""

    def __init__(self, data):
        """Initalize the Class."""
        self.data = data
        self.front_diameter = DoubleVar()
        self.back_diameter = DoubleVar()
        self.length = QuantityVar(unit="m")
        self.volume_total = QuantityVar(unit="m³")
        self.volume_propellant_H2O = QuantityVar(unit="m³")
        self.volume_propellant_D2 = QuantityVar(unit="m³")
        self.volume_propellant_H3 = QuantityVar(unit="m³")
        self.volume_lifesupport = QuantityVar(unit="m³")
        self.volume_reactors = QuantityVar(unit="m³")
        self.volume_thrusters = QuantityVar(unit="m³")
        self.volume_aux_thrusters = QuantityVar(unit="m³")

    def make_entry(self, frame):
        """Make the Entry Form."""
        entry = {
            "Front Diameter": {
                "value": self.front_diameter,
                "unit": "m"
            },
            "Rear Diameter": {
                "value": self.back_diameter,
                "unit": "m"
            },
        }
        self._make_entry(frame, "Propulsion", entry)

    def make_display(self, frame):
        """Make the Data Display."""
        data = {
            "Volume Propellant (H2O)": {
                "value": self.volume_propellant_H2O,
            },
            "Volume Propellant (Helium_3)": {
                "value": self.volume_propellant_H3,
            },
            "Volume Propellant (Deuterium)": {
                "value": self.volume_propellant_D2,
            },
            "Volume Lifesupport": {
                "value": self.volume_lifesupport,
            },
            "Volume Reactors": {
                "value": self.volume_reactors,
            },
            "Volume Thrusters": {
                "value": self.volume_thrusters,
            },
            "Volume Auxiliary Thrusters": {
                "value": self.volume_aux_thrusters,
            },
            "Volume Total": {
                "value": self.volume_total,
            },
        }
        self._make_display(frame, "Propulsion Data", data)

    def calculate(self):
        """Do the calculations."""
        print("Calculate!")
        volume_H2O = self.data.volumes["Propellant H2O"]
        volume_H3 = self.data.volumes["Propellant H3"]
        volume_D2 = self.data.volumes["Propellant D2"]
        volume_lifesupport = self.data.volumes["Lifesupport"]
        volume_thrusters = self.data.volumes["Propulsion"]
        volume_reactors = self.data.volumes["Reactors"]
        volume_aux_thrusters = self.data.volumes["Auxiliary Thrusters"]
        volume_total = 0
        for _, subsystem in self.data.volumes.items():
            volume_total += subsystem
        self.volume_total.set(volume_total)
        self.volume_propellant_H2O.set(volume_H2O)
        self.volume_propellant_H3.set(volume_H3)
        self.volume_propellant_D2.set(volume_D2)
        self.volume_lifesupport.set(volume_lifesupport)
        self.volume_reactors.set(volume_reactors)
        self.volume_thrusters.set(volume_thrusters)
        self.volume_aux_thrusters.set(volume_aux_thrusters)
