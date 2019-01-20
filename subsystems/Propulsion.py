"""Propulsion Class."""

from tkinter import DoubleVar, IntVar
from subsystems.Subsystem import Subsystem
from widgets.QuantityVar import QuantityVar


class Propulsion(Subsystem):
    """Contains the Propulsion Data."""

    def __init__(self, data):
        """Init the Propulsion."""
        self.data = data
        self.propulsion = data.propulsion
        self.max_acceleration = DoubleVar()
        self.no_thrusters = IntVar(value=2)
        self.power_thruster = DoubleVar(value=750)
        self.power_total_thruster = QuantityVar(unit="W")
        self.mass_total_thruster = QuantityVar(unit="g")
        self.waste_power = QuantityVar(unit="W")

    def make_entry(self, frame):
        """Make the Entry Form."""
        entry = {
            "Max Acceneration": {
                "value": self.max_acceleration,
                "unit": "m/s²"
            },
            "Thruster Power": {
                "value": self.power_thruster,
                "unit": "GW"
            },
            "Number of Thrusters": {
                "value": self.no_thrusters,
                "unit": ""
            },
        }
        self._make_entry(frame, "Propulsion", entry)

    def make_display(self, frame):
        """Make the Data Display."""
        data = {
            "Total Thruster Power": {
                "value": self.power_total_thruster,
            },
            "Total Thruster Mass": {
                "value": self.mass_total_thruster,
            },
            "Retained Waste Power": {
                "value": self.waste_power,
            }
        }
        self._make_display(frame, "Propulsion Data", data)

    def calculate(self):
        """Do the calculations."""
        power_thruster = self.power_thruster.get() * 1e9
        # max_acceleration = self.max_acceleration.get()
        no_thrusters = self.no_thrusters.get()
        mass_thruster = power_thruster * self.propulsion["Thruster Mass"] / 1e6
        power_total_thruster = power_thruster * no_thrusters
        mass_total_thruster = mass_thruster * no_thrusters
        waste_power = power_total_thruster * self.propulsion["Waste Factor"]
        self.data.masses["Thrusters"] = mass_total_thruster
        self.data.wasteheat["Thrusters"] = waste_power

        self.mass_total_thruster.set(mass_total_thruster)
        self.power_total_thruster.set(power_total_thruster)
        self.waste_power.set(waste_power)
