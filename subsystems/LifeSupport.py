"""LifeSupport class."""

from widgets.MultiDisplay import MultiDisplay
from tkinter import DoubleVar, IntVar
from subsystems.Radiator import Radiator
from subsystems.Subsystem import Subsystem
from widgets.QuantityVar import QuantityVar


class LifeSupport(Subsystem):
    """Contains the Life Support Data."""

    def __init__(self, data):
        """Init the Life Support."""
        self.data = data
        self.life_support_data = data.life_support
        self.crew = IntVar()
        self.endurance = IntVar()
        self.mass_supplies_nonrenewable = QuantityVar(unit="g")
        self.mass_supplies_renewable = QuantityVar(unit="g")
        self.mass_supplies = QuantityVar(unit="g")
        self.volume_habitat = QuantityVar(unit="m³")
        self.mass_habitat = QuantityVar(unit="g")
        self.volume_supplies = QuantityVar(unit="m³")
        self.volume_total = QuantityVar(unit="m³")
        self.mass_total = QuantityVar(unit="g")
        self.power_requirements = QuantityVar(unit="W")
        self.radiator = Radiator(data, "Life Support")

    def make_entry(self, frame):
        """Create the Entry Form for Data."""
        entry = {
            "Crew size": {
                "value": self.crew,
                "unit": ""
            },
            "Endurance": {
                "value": self.endurance,
                "unit": "days",
                "type": "Spinbox",
                "config": {
                    "from": 30,
                    "to": 50 * 30,
                    "increment": 30
                }
            }
        }
        self._make_entry(frame, "Crew", entry)

    def make_display(self, frame):
        """Create the Data Display for Data."""
        self.data_display = MultiDisplay(frame, "Crew Data")
        self.radiator.make_display(self.data_display.frame)
        data = {
            "Non-Renewable Supplies": {
                "value": self.mass_supplies_nonrenewable,
            },
            "Renewable Supplies": {
                "value": self.mass_supplies_renewable,
            },
            "Supplies Volume": {
                "value": self.volume_supplies,
            },
            "Total Supplies Mass": {
                "value": self.mass_supplies,
            },
            "Habitat Volume": {
                "value": self.volume_habitat,
            },
            "Habitat Mass": {
                "value": self.mass_habitat,
            },
            "Total Volume": {
                "value": self.volume_total,
            },
            "Total Mass": {
                "value": self.mass_total,
            },
            "Energy Requirements": {
                "value": self.power_requirements,
            },
            "Radiator": {
                "value": self.radiator.data_display
            }
        }
        self.data_display.make_display(data)
        self.data_display.frame.grid(column=1, row=1, sticky='new', padx=5)

    def calculate(self):
        """Calculates the Life support Data."""
        crew = self.crew.get()
        endurance = self.endurance.get()
        mass_supplies_nonrenewable = crew * endurance \
            * self.life_support_data["Non-renewable Supplies"] * 1000
        mass_supplies_renewable = crew * endurance * \
            self.life_support_data["Renewable Supplies"] * 1000
        volume_habitat = crew * self.life_support_data["Habitat Volume"]
        mass_habitat = volume_habitat * self.life_support_data["Habitat Mass"] \
            * 1000
        volume_supplies = (mass_supplies_renewable + mass_supplies_nonrenewable) \
            / self.life_support_data["Supply Volume"] / 1000
        waste_heat = crew * self.life_support_data["Waste Heat"] * 1e3
        self.radiator.calculate(waste_heat)
        power_requirements = crew * \
            self.life_support_data["Energy Requirements"] * 1e6
        volume_total = (volume_supplies + volume_habitat) * 1.1
        mass_total = mass_habitat + mass_supplies_renewable + mass_supplies_nonrenewable
        self.data.masses["Lifesupport Mass"] = mass_total

        # Change the Labels
        self.mass_supplies_nonrenewable.set(mass_supplies_nonrenewable)
        self.mass_supplies_renewable.set(mass_supplies_renewable)
        self.mass_supplies.set(mass_supplies_renewable + mass_supplies_nonrenewable)
        self.volume_habitat.set(volume_habitat)
        self.volume_supplies.set(volume_supplies)
        self.volume_total.set(volume_total)
        self.mass_habitat.set(mass_habitat)
        self.mass_total.set(mass_total)
        self.power_requirements.set(power_requirements)
        self.data.power_lifesupport = power_requirements
