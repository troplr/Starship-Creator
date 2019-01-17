"""PowerGeneration class."""

from widgets.MultiEntry import MultiEntry
from widgets.MultiDisplay import MultiDisplay
from tkinter import DoubleVar, IntVar
from subsystems.Subsystem import Subsystem


class PowerGeneration(Subsystem):
    """Contains all Data on Power Generation."""

    def __init__(self, data):
        """Init the Power Generation."""
        self.data = data
        self.powergeneration = data.powergeneration
        efficiency = self.powergeneration["Reactor Efficiency"]
        self.no_reactors = IntVar(value=1)
        self.power_need = DoubleVar()
        self.power_reactor = DoubleVar()
        self.mass_reactor = DoubleVar()
        self.power_overall = DoubleVar()
        self.power_effective = DoubleVar()
        self.waste_heat = DoubleVar()
        self.mass_total_reactor = DoubleVar()
        self.efficiency = DoubleVar(value=efficiency)

        self.make_entry()
        self.make_display()

    def make_entry(self):
        """Make the Entry Form."""
        entry = {
            "Number of Reactors": {
                "value": self.no_reactors,
                "unit": ""
            }
        }
        self.entry = MultiEntry(self.data.main_frame, "Power Generation", entry)

    def make_display(self):
        """Make the Data Display."""
        data = {
            "Power Needed": {
                "value": self.power_need,
                "unit": "MW"
            },
            "Reactor Efficiency": {
                "value": self.efficiency,
                "unit": ""
            },
            "Overall Reactor Power": {
                "value": self.power_overall,
                "unit": "MW"
            },
            "Power per Reactor": {
                "value": self.power_reactor,
                "unit": "MW"
            },
            "Effective Power Overall": {
                "value": self.power_effective,
                "unit": "MW"
            },
            "Waste Heat": {
                "value": self.waste_heat,
                "unit": "MW"
            },
            "Mass per Reactor": {
                "value": self.mass_reactor,
                "unit": "kg"
            },
            "Total Reactor Mass": {
                "value": self.mass_total_reactor,
                "unit": "kg"
            },
        }
        self.data_display = MultiDisplay(self.data.main_frame, "Reactor Data")
        self.data_display.make_display(data)

    def calculate(self):
        """Do the calculation."""
        no_reactors = self.no_reactors.get()
        efficiency = self.efficiency.get()
        reactor_mass = self.powergeneration["Reactor Mass"]
        power_need = self.data.power_lifesupport + \
            self.data.power_weapons + \
            self.data.power_aux_thrusters
        power_effective_need = power_need / efficiency
        power_reactors = self._roundup(x=power_effective_need, next_largest=500)
        power_reactor = self._roundup(x=power_reactors / no_reactors, next_largest=250)
        power_overall = power_reactor * no_reactors
        power_effective = power_overall * efficiency
        waste_heat = power_overall - power_effective
        mass_reactor = power_reactor * reactor_mass
        mass_total = mass_reactor * no_reactors
        self.power_need.set(power_need)
        self.power_overall.set(power_overall)
        self.power_reactor.set(power_reactor)
        self.mass_reactor.set(mass_reactor)
        self.power_effective.set(power_effective)
        self.waste_heat.set(waste_heat)
        self.mass_total_reactor.set(mass_total)
