"""Main Spacecraft class."""
from tkinter import DoubleVar, IntVar, StringVar
from widgets.MultiEntry import MultiEntry
from widgets.MultiDisplay import MultiDisplay
from subsystems.LifeSupport import LifeSupport
from subsystems.Propulsion import Propulsion
from subsystems.PowerGeneration import PowerGeneration
from subsystems.Subsystem import Subsystem


class Spacecraft(Subsystem):
    """Spacecraft Class."""

    def __init__(self, data):
        """Init the Spacecraft."""
        self.data = data
        self.subsections = {
            "Lifesupport": LifeSupport(data),
            "Propulsion": Propulsion(data),
            "Power Generation": PowerGeneration(data),
        }
        self.no_reactors = IntVar()
        self.mass_ratio = DoubleVar()
        self.mass_armor = DoubleVar()
        self.mass_defensive = DoubleVar()
        self.mass_cargo = DoubleVar()
        self.mass_other = DoubleVar()
        self.mass_lifesupport = StringVar()
        self.mass_propulsion = StringVar()
        self.mass_reactor = StringVar()
        self.mass_total_dry = StringVar()
        self.mass_total_wet = StringVar()
        self.mass_propellant = StringVar()

    def calculate(self):
        """Calculates the spacecraft."""
        for _, subsection in self.subsections.items():
            subsection.calculate()
        mass_lifesupport = self.subsections["Lifesupport"].mass_supplies.get() + \
            self.subsections["Lifesupport"].mass_habitat.get() + \
            self.subsections["Lifesupport"].radiator.mass.get()
        mass_propulsion = self.subsections["Propulsion"].mass_total_thruster.get()
        mass_reactor = self.subsections["Power Generation"].mass_total_reactor.get()
        mass_total_dry = self.mass_armor.get() + \
            self.mass_cargo.get() + \
            self.mass_other.get() + \
            self.mass_defensive.get() + \
            mass_propulsion + \
            mass_lifesupport + \
            mass_reactor
        mass_propellant = mass_total_dry
        mass_total_wet = mass_total_dry + mass_propellant
        self.mass_lifesupport.set(self._format_number(mass_lifesupport))
        self.mass_propulsion.set(self._format_number(mass_propulsion))
        self.mass_reactor.set(self._format_number(mass_reactor))
        self.mass_total_dry.set(self._format_number(mass_total_dry))
        self.mass_total_wet.set(self._format_number(mass_total_wet))

    def make_entry(self, root):
        """Creates the Multi Entry Widget."""
        column = 0
        for _, subsection in self.subsections.items():
            subsection.entry.frame.grid(column=column, row=0, sticky='new', padx=5)
            column = column + 1
        entry = {
            "Armor Mass": {
                "value": self.mass_armor,
                "unit": "kg"
            },
            "Cargo Mass": {
                "value": self.mass_cargo,
                "unit": "kg"
            },
            "Other Mass": {
                "value": self.mass_other,
                "unit": "kg"
            }
        }
        self.entry = MultiEntry(root, "Other Entries", entry)
        self.entry.frame.grid(column=column, row=0, sticky='new', padx=5)

    def make_display(self, root):
        """Creates the Multi Display Widget."""
        column = 0
        for _, subsection in self.subsections.items():
            subsection.data_display.frame.grid(column=column, row=1, sticky='new', padx=5)
            column = column + 1
        data = {
            "Overall Lifesupport Mass": {
                "value": self.mass_lifesupport,
                "unit": "kg"
            },
            "Overall Propulsion Mass": {
                "value": self.mass_propulsion,
                "unit": "kg"
            },
            "Overall Reactor Mass": {
                "value": self.mass_reactor,
                "unit": "kg"
            },
            "Propellant Mass": {
                "value": self.mass_propellant,
                "unit": "kg"
            },
            "Total Dry Mass": {
                "value": self.mass_total_dry,
                "unit": "kg"
            },
            "Total Wet Mass": {
                "value": self.mass_total_wet,
                "unit": "kg"
            }
        }
        self.data_display = MultiDisplay(root, "Masses")
        self.data_display.make_display(data)
        self.data_display.frame.grid(column=column, row=1, sticky='new', padx=5)
