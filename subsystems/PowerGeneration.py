"""PowerGeneration class."""

from tkinter import DoubleVar, IntVar
from subsystems.Subsystem import Subsystem
from widgets.QuantityVar import QuantityVar


class PowerGeneration(Subsystem):
    """Contains all Data on Power Generation."""

    def __init__(self, data):
        """Init the Power Generation."""
        self.data = data
        self.powergeneration = data.powergeneration
        efficiency = self.powergeneration["Reactor Efficiency"]
        self.no_reactors = IntVar(value=1)
        self.power_need = QuantityVar(unit="W")
        self.power_reactor = DoubleVar()
        self.mass_reactor = QuantityVar(unit="g")
        self.power_overall = QuantityVar(unit="W")
        self.power_effective = QuantityVar(unit="W")
        self.waste_heat = QuantityVar(unit="W")
        self.mass_total_reactor = QuantityVar(unit="g")
        self.efficiency = DoubleVar(value=efficiency)

    def make_entry(self, frame):
        """Make the Entry Form."""
        entry = {
            "Power per Reactor": {
                "value": self.power_reactor,
                "unit": "MW",
                "type": "Spinbox",
                "config": {
                    "from": 50,
                    "to": 100 * 50,
                    "increment": 50
                }
            }
        }
        self._make_entry(frame, "Power Generation", entry)

    def make_display(self, frame):
        """Make the Data Display."""
        data = {
            "Power Needed": {
                "value": self.power_need,
            },
            "Reactor Efficiency": {
                "value": self.efficiency,
            },
            "Needed Ractors": {
                "value": self.no_reactors,
            },
            "Overall Reactor Power": {
                "value": self.power_overall,
            },
            "Effective Power Overall": {
                "value": self.power_effective,
            },
            "Waste Heat": {
                "value": self.waste_heat,
            },
            "Mass per Reactor": {
                "value": self.mass_reactor,
            },
            "Total Reactor Mass": {
                "value": self.mass_total_reactor,
            },
        }
        self._make_display(frame, "Reactor Data", data)

    def calculate(self):
        """Do the calculation."""
        efficiency = self.efficiency.get()
        power_reactor = self.power_reactor.get() * 1e6
        reactor_mass = self.powergeneration["Reactor Mass"] / 1000
        power_need = 0
        for _, subsystem in self.data.power.items():
            power_need += subsystem
        power_effective = power_need
        power_overall = self._roundup(power_need / efficiency, power_reactor)
        no_reactors = power_overall / power_reactor
        print(power_need, ', ', power_overall, ', ', no_reactors)
        waste_heat = power_overall - power_effective
        mass_reactor = power_reactor * reactor_mass
        mass_total = mass_reactor * no_reactors
        self.data.masses["Reactors"] = mass_total
        print(mass_reactor)
        self.power_need.set(power_need)
        self.no_reactors.set(no_reactors)
        self.power_overall.set(power_overall)
        self.mass_reactor.set(mass_reactor)
        self.power_effective.set(power_effective)
        self.waste_heat.set(waste_heat)
        self.mass_total_reactor.set(mass_total)
