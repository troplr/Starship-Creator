"""Class for Auxiliary Thrusters."""

from tkinter import IntVar, StringVar
from subsystems.Subsystem import Subsystem
from widgets.QuantityVar import QuantityVar


class AuxThrusters(Subsystem):
    """Class for Auxiliary Thrusters."""

    def __init__(self, data):
        """Initialize the class."""
        self.data = data
        self.aux_thrusters = data.aux_thrusters
        self.aux_thruster = StringVar()
        self.power_aux_thrusters = QuantityVar(unit='W')
        self.mass_aux_thrusters = QuantityVar(unit='g')
        self.thrust_aux_thrusters = QuantityVar(unit='N')
        self.no_thrusters = IntVar(value=6 * 4)
        self.power_total = QuantityVar(unit='W')
        self.mass_total = QuantityVar(unit='g')
        self.thrust_total_direction = QuantityVar(unit='N')

    def make_entry(self, frame):
        """Make the Data Entry."""
        entry = {
            "Auxiliary Thruster": {
                "value": self.aux_thruster,
                "unit": "",
                "type": "Combobox",
                "list": [key for key in self.aux_thrusters]
            }
        }
        self._make_entry(frame, "Auxiliary Thruster", entry)

    def make_display(self, frame):
        """Make the Data Display."""
        data = {
            "Auxiliary Thruster Power": {
                "value": self.power_aux_thrusters,
            },
            "Auxiliary Thruster Mass": {
                "value": self.mass_aux_thrusters,
            },
            "Thrust per Auxiliary Thruster": {
                "value": self.thrust_aux_thrusters,
            },
            "Number of Auxiliary Thrusters": {
                "value": self.no_thrusters,
            },
            "Total Auxiliary Thruster Power": {
                "value": self.power_total,
            },
            "Total Auxiliary Thruster Mass": {
                "value": self.mass_total,
            },
            "Total Thrust per Direction": {
                "value": self.thrust_total_direction,
            }
        }
        self._make_display(frame, "Auxiliary Thruster", data)

    def calculate(self):
            """Calculates the Data."""
            thruster = self.aux_thruster.get()
            thruster_data = self.aux_thrusters[thruster]
            power_aux_thrusters = thruster_data['Power'] * 1e6
            mass_aux_thrusters = thruster_data['Thruster Mass'] * 1e3
            thrust_aux_thrusters = thruster_data['Thrust'] * 1e3
            no_thrusters = self.no_thrusters.get()
            power_total = no_thrusters * power_aux_thrusters
            mass_total = no_thrusters * mass_aux_thrusters
            thrust_total_direction = no_thrusters * thrust_aux_thrusters / 6
            self.data.masses["Auxiliary Thrusters"] = mass_total
            self.data.power["Auxiliary Thrusters"] = power_total
            self.power_aux_thrusters.set(power_aux_thrusters)
            self.mass_aux_thrusters.set(mass_aux_thrusters)
            self.thrust_aux_thrusters.set(thrust_aux_thrusters)
            self.power_total.set(power_total)
            self.mass_total.set(mass_total)
            self.thrust_total_direction.set(thrust_total_direction)
