"""LifeSupport class."""

from widgets.MultiDisplay import MultiDisplay
from tkinter import DoubleVar, IntVar
from subsystems.Radiator import Radiator
from subsystems.Subsystem import Subsystem


class LifeSupport(Subsystem):
    """Contains the Life Support Data."""

    def __init__(self, data):
        """Init the Life Support."""
        self.data = data
        self.life_support_data = data.life_support
        self.crew = IntVar()
        self.endurance = IntVar()
        self.mass_supplies_nonrenewable = DoubleVar()
        self.mass_supplies_renewable = DoubleVar()
        self.mass_supplies = DoubleVar()
        self.volume_habitat = DoubleVar()
        self.mass_habitat = DoubleVar()
        self.volume_supplies = DoubleVar()
        self.power_requirements = DoubleVar()
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
                "unit": "days"
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
                "unit": "kg"
            },
            "Renewable Supplies": {
                "value": self.mass_supplies_renewable,
                "unit": "kg"
            },
            "Supplies Volume": {
                "value": self.volume_supplies,
                "unit": "m³"
            },
            "Total Supplies Mass": {
                "value": self.mass_supplies,
                "unit": "kg"
            },
            "Habitat Volume": {
                "value": self.volume_habitat,
                "unit": "m³"
            },
            "Habitat Mass": {
                "value": self.mass_habitat,
                "unit": "kg"
            },
            "Energy Requirements": {
                "value": self.power_requirements,
                "unit": "MW"
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
            * self.life_support_data["Non-renewable Supplies"]
        mass_supplies_renewable = crew * endurance * \
            self.life_support_data["Renewable Supplies"]
        volume_habitat = crew * self.life_support_data["Habitat Volume"]
        mass_habitat = volume_habitat * self.life_support_data["Habitat Mass"]
        volume_supplies = (mass_supplies_renewable + mass_supplies_nonrenewable) \
            / self.life_support_data["Supply Volume"]
        waste_heat = crew * self.life_support_data["Waste Heat"] * 1e3
        self.radiator.calculate(waste_heat)
        power_requirements = crew * self.life_support_data["Energy Requirements"]
        print(mass_habitat, ", ", mass_supplies_renewable, ", ", mass_supplies_nonrenewable, ", ", mass_habitat + mass_supplies_renewable + mass_supplies_nonrenewable)
        # Change the Labels
        self.mass_supplies_nonrenewable.set(mass_supplies_nonrenewable)
        self.mass_supplies_renewable.set(mass_supplies_renewable)
        self.mass_supplies.set(mass_supplies_renewable + mass_supplies_nonrenewable)
        self.volume_habitat.set(volume_habitat)
        self.volume_supplies.set(volume_supplies)
        self.mass_habitat.set(mass_habitat)
        self.power_requirements.set(power_requirements)
        self.data.power_lifesupport = power_requirements
