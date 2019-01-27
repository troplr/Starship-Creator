"""Main Spacecraft class."""
from tkinter import DoubleVar, IntVar
from subsystems.LifeSupport import LifeSupport
from subsystems.Propulsion import Propulsion
from subsystems.PowerGeneration import PowerGeneration
from subsystems.AuxThrusters import AuxThrusters
from subsystems.Subsystem import Subsystem
from subsystems.Radiator import Radiator
from subsystems.VelocityProfile import VelocityProfile
from subsystems.Size import Size
from widgets.QuantityVar import QuantityVar


class Spacecraft(Subsystem):
    """Spacecraft Class."""

    def __init__(self, data):
        """Init the Spacecraft."""
        self.data = data
        self.subsections = {
            "Lifesupport": LifeSupport(data),
            "Propulsion": Propulsion(data),
            "Aux Thrusters": AuxThrusters(data),
            "Power Generation": PowerGeneration(data),
            "Radiators": Radiator(data, "Microtube Array"),
        }
        self.no_reactors = IntVar()
        self.mass_ratio = DoubleVar(value=3)
        self.mass_armor = DoubleVar()
        self.mass_defensive = DoubleVar()
        self.mass_cargo = DoubleVar()
        self.mass_other = DoubleVar()
        self.mass_lifesupport = QuantityVar(unit="g")
        self.mass_propulsion = QuantityVar(unit="g")
        self.mass_reactor = QuantityVar(unit="g")
        self.mass_aux_thrusters = QuantityVar(unit="g")
        self.mass_total_dry = QuantityVar(unit="g")
        self.mass_total_wet = QuantityVar(unit="g")
        self.mass_propellant = QuantityVar(unit="g")
        self.mass_H2O = QuantityVar(unit="g")
        self.mass_H3 = QuantityVar(unit="g")
        self.mass_D2 = QuantityVar(unit="g")
        self.sizes = Size(data)
        self.velocities = VelocityProfile(data)

    def calculate(self):
        """Calculates the spacecraft."""
        for _, subsection in self.subsections.items():
            subsection.calculate()
        mass_lifesupport = self.data.masses["Lifesupport"]
        mass_propulsion = self.data.masses["Thrusters"]
        mass_reactor = self.data.masses["Reactors"]
        mass_aux_thrusters = self.data.masses["Auxiliary Thrusters"]
        mass_total_dry = self.mass_armor.get() + \
            self.mass_cargo.get() + \
            self.mass_other.get() + \
            self.mass_defensive.get() + \
            mass_aux_thrusters + \
            mass_propulsion + \
            mass_lifesupport + \
            mass_reactor
        mass_propellant = mass_total_dry * self.mass_ratio.get()
        mass_total_wet = mass_total_dry + mass_propellant
        mass_H3 = mass_propellant / 750
        mass_D2 = mass_H3 * 1.25
        mass_H2O = mass_propellant - mass_D2 - mass_H3
        volume_H3 = mass_H3 / (442.7 * 1e3)
        volume_D2 = mass_D2 / (169 * 1e3)
        volume_H2O = mass_H2O / (1000 * 1e3)
        self.data.volumes["Propellant H2O"] = volume_H2O
        self.data.volumes["Propellant H3"] = volume_H3
        self.data.volumes["Propellant D2"] = volume_D2
        self.data.thruster_data["Mass Ratio"] = self.mass_ratio.get()
        self.data.thruster_data["Mass"] = mass_total_wet
        self.sizes.calculate()
        self.velocities.calculate()

        self.mass_lifesupport.set(mass_lifesupport)
        self.mass_propulsion.set(mass_propulsion)
        self.mass_reactor.set(mass_reactor)
        self.mass_total_dry.set(mass_total_dry)
        self.mass_propellant.set(mass_propellant)
        self.mass_total_wet.set(mass_total_wet)
        self.mass_aux_thrusters.set(mass_aux_thrusters)
        self.mass_H2O.set(mass_H2O)
        self.mass_D2.set(mass_D2)
        self.mass_H3.set(mass_H3)

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
            },
            "Mass Ratio": {
                "value": self.mass_ratio,
                "unit": ""
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
            "Overall Auxiliary Thruster Mass": {
                "value": self.mass_aux_thrusters,
            },
            "Overall Reactor Mass": {
                "value": self.mass_reactor,
            },
            "Propellant Mass": {
                "value": self.mass_propellant,
            },
            "Propellant Mass (H2O)": {
                "value": self.mass_H2O,
            },
            "Propellant Mass (Helium-3)": {
                "value": self.mass_H3,
            },
            "Propellant Mass (Deuterium)": {
                "value": self.mass_D2,
            },
            "Total Dry Mass": {
                "value": self.mass_total_dry,
            },
            "Total Wet Mass": {
                "value": self.mass_total_wet,
            }
        }
        self._make_display(frame, "Masses", data)
