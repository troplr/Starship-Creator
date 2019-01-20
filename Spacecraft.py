"""Main Spacecraft class."""
from tkinter import DoubleVar, IntVar, StringVar
from subsystems.LifeSupport import LifeSupport
from subsystems.Propulsion import Propulsion
from subsystems.PowerGeneration import PowerGeneration
from subsystems.Subsystem import Subsystem
from widgets.QuantityVar import QuantityVar


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
        self.mass_lifesupport = QuantityVar(unit="g")
        self.mass_propulsion = QuantityVar(unit="g")
        self.mass_reactor = QuantityVar(unit="g")
        self.mass_total_dry = QuantityVar(unit="g")
        self.mass_total_wet = QuantityVar(unit="g")
        self.mass_propellant = QuantityVar(unit="g")

    def calculate(self):
        """Calculates the spacecraft."""
        for _, subsection in self.subsections.items():
            subsection.calculate()
        mass_lifesupport = self.data.masses["Lifesupport Mass"]
        mass_propulsion = self.data.masses["Mass Thrusters"]
        mass_reactor = self.data.masses["Total Reactor"]
        mass_total_dry = self.mass_armor.get() + \
            self.mass_cargo.get() + \
            self.mass_other.get() + \
            self.mass_defensive.get() + \
            mass_propulsion + \
            mass_lifesupport + \
            mass_reactor
        mass_propellant = mass_total_dry
        mass_total_wet = mass_total_dry + mass_propellant
        self.mass_lifesupport.set(mass_lifesupport)
        self.mass_propulsion.set(mass_propulsion)
        self.mass_reactor.set(mass_reactor)
        self.mass_total_dry.set(mass_total_dry)
        self.mass_total_wet.set(mass_total_wet)

    def make_entry(self, frame):
        """Creates the Multi Entry Widget."""
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
        self._make_entry(frame, "Other Entries", entry)

    def make_display(self, frame):
        """Creates the Multi Display Widget."""
        data = {
            "Overall Lifesupport Mass": {
                "value": self.mass_lifesupport,
            },
            "Overall Propulsion Mass": {
                "value": self.mass_propulsion,
            },
            "Overall Reactor Mass": {
                "value": self.mass_reactor,
            },
            "Propellant Mass": {
                "value": self.mass_propellant,
            },
            "Total Dry Mass": {
                "value": self.mass_total_dry,
            },
            "Total Wet Mass": {
                "value": self.mass_total_wet,
            }
        }
        self._make_display(frame, "Masses", data)
