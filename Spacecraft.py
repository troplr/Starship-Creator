"""
Main Spacecraft class.
"""
from tkinter import DoubleVar, IntVar, StringVar
from MultiEntry import MultiEntry
from MultiDisplay import MultiDisplay
from math import ceil


def roundup(x, next_largest):
    return float(ceil(x / next_largest)) * next_largest


class Spacecraft():
    """ """

    def __init__(self, data):
        """ Init the Spacecraft """
        self.data = data
        self.subsections = {
            "Lifesupport": LifeSupport(data),
            "Propulsion": Propulsion(data),
            "Power Generation": PowerGeneration(data),
        }
        self.no_reactors = IntVar(value=0)
        self.mass_ratio = DoubleVar(value=0)
        self.mass_armor = DoubleVar(value=0)
        self.mass_defensive = DoubleVar(value=0)
        self.mass_cargo = DoubleVar(value=0)
        self.mass_other = DoubleVar(value=0)
        self.mass_lifesupport = DoubleVar(value=0)
        self.mass_propulsion = DoubleVar(value=0)
        self.mass_reactor = DoubleVar()
        self.mass_total_dry = DoubleVar()
        self.mass_total_wet = DoubleVar()
        self.mass_propellant = DoubleVar()

    def calculate(self):
        """ Calculates the spacecraft """
        for _, subsection in self.subsections.items():
            subsection.calculate()
        self.mass_lifesupport.set(
            self.subsections["Lifesupport"].mass_supplies.get()
            + self.subsections["Lifesupport"].mass_habitat.get()
            + self.subsections["Lifesupport"].radiator.mass.get()
        )
        self.mass_propulsion.set(
            self.subsections["Propulsion"].mass_total_thruster.get()
        )
        self.mass_reactor.set(
            self.subsections["Power Generation"].mass_total_reactor.get()
        )
        self.mass_total_dry.set(
            self.mass_armor.get()
            + self.mass_cargo.get()
            + self.mass_other.get()
            + self.mass_defensive.get()
            + self.mass_propulsion.get()
            + self.mass_lifesupport.get()
            + self.mass_reactor.get()
        )
        self.mass_total_wet.set(
            self.mass_total_dry.get()
            + self.mass_propellant.get()
        )

    def make_entry(self, root):
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
            },
        }
        self.entry = MultiEntry(root, "Other Entries", entry)
        self.entry.frame.grid(column=column, row=0, sticky='new', padx=5)

    def make_display(self, root):
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


class PowerGeneration():
    """
    Contains all Data on Power Generation.
    """

    def __init__(self, data):
        """ Init the Power Generation. """
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
        """ Make the Entry Form """
        entry = {
            "Number of Reactors": {
                "value": self.no_reactors,
                "unit": ""
            }
        }
        self.entry = MultiEntry(self.data.main_frame, "Power Generation", entry)

    def make_display(self):
        """ Make the Data Display """
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
        """ Do the calculation """
        no_reactors = self.no_reactors.get()
        efficiency = self.efficiency.get()
        reactor_mass = self.powergeneration["Reactor Mass"]
        power_need = self.data.power_lifesupport + \
            self.data.power_weapons + \
            self.data.power_aux_thrusters
        print(power_need)
        power_effective_need = power_need / efficiency
        print(power_effective_need)
        power_reactors = roundup(power_effective_need, 500)
        print(power_reactors)
        power_reactor = roundup(power_reactors / no_reactors, 250)
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


class Propulsion():
    """ Contains the Propulsion Data """

    def __init__(self, data):
        """ Init the Propulsion """
        self.data = data
        self.propulsion = data.propulsion
        self.max_acceleration = DoubleVar(value=0)
        self.no_thrusters = IntVar(value=2)
        self.power_thruster = DoubleVar(value=750)
        self.power_total_thruster = DoubleVar()
        self.mass_total_thruster = DoubleVar()
        self.waste_power = DoubleVar()

        self.make_entry()
        self.make_display()

    def make_entry(self):
        """ Make the Entry Form """
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
        self.entry = MultiEntry(self.data.main_frame, "Propulsion", entry)

    def make_display(self):
        """ Make the Data Display """
        data = {
            "Total Thruster Power": {
                "value": self.power_total_thruster,
                "unit": "GW"
            },
            "Total Thruster Mass": {
                "value": self.mass_total_thruster,
                "unit": "kg"
            },
            "Retained Waste Power": {
                "value": self.waste_power,
                "unit": "GW"
            }
        }
        self.data_display = MultiDisplay(self.data.main_frame, "Propulsion Data")
        self.data_display.make_display(data)

    def calculate(self):
        """ Do the calculations """
        power_thruster = self.power_thruster.get()
        max_acceleration = self.max_acceleration.get()
        no_thrusters = self.no_thrusters.get()
        mass_thruster = power_thruster * self.propulsion["Thruster Mass"]
        power_total_thruster = power_thruster * no_thrusters
        mass_total_thruster = mass_thruster * no_thrusters
        waste_power = power_thruster * self.propulsion["Waste Factor"]

        self.mass_total_thruster.set(mass_total_thruster)
        self.power_total_thruster.set(power_total_thruster)
        self.waste_power.set(waste_power)


class LifeSupport():
    """ Contains the Life Support Data """

    def __init__(self, data):
        """ Init the Life Support """
        self.data = data
        self.life_support_data = data.life_support
        self.crew = IntVar(value=0)
        self.endurance = IntVar(value=0)
        self.mass_supplies_nonrenewable = DoubleVar(value=0)
        self.mass_supplies_renewable = DoubleVar(value=0)
        self.mass_supplies = DoubleVar(value=0)
        self.volume_habitat = DoubleVar(value=0)
        self.mass_habitat = DoubleVar(value=0)
        self.volume_supplies = DoubleVar(value=0)
        self.power_requirements = DoubleVar(value=0)
        self.radiator = Radiator(data, "Life Support")
        self.make_entry()
        self.make_display()

    def make_entry(self):
        """ Create the Entry Form for Data """
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
        self.entry = MultiEntry(self.data.main_frame, "Crew", entry)

    def make_display(self):
        """ Create the Data Display for Data """
        self.data_display = MultiDisplay(self.data.main_frame, "Crew Data")
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

    def calculate(self):
        """ Calculates the Life support Data """
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


class Radiator():
    """ Contains Radiator Data """

    def __init__(self, data, type):
        """ Init the Radiator """
        self.data = data
        self.radiators = data.radiators
        self.radiator_data = data.radiators[type]
        self.radiators_type = StringVar(value=type)
        self.mass = DoubleVar(value=0)
        self.area = DoubleVar(value=0)
        self.waste_heat = DoubleVar(value=0)

    def make_display(self):
        """ Creates the Entry for Radiator Stuff """

    def make_display(self, root=None):
        """ Creates the Display for the Radiator Stuff """
        data = {
            "Radiator Type": {
                "value": self.radiators_type,
                "unit": ""
            },
            "Waste Heat": {
                "value": self.waste_heat,
                "unit": "kW"
            },
            "Area": {
                "value": self.area,
                "unit": "m²"
            },
            "Mass": {
                "value": self.mass,
                "unit": "kg"
            }
        }
        if not root:
            root = self.data_display
        self.data_display = MultiDisplay(root, "Life Support Radiators")
        self.data_display.make_display(data)

    def calculate(self, waste_heat):
        """ Calculates the Radiator Data """
        self.waste_heat.set(waste_heat / 1e3)
        area = waste_heat / self.radiator_data["Specific area heat"]
        mass = waste_heat / self.radiator_data["Specific area mass"]
        self.area.set(area)
        self.mass.set(mass)

    def change_radiator(self, type):
        """ Change the radiator type """
        self.radiator_data = self.radiators[type]
        self.radiators_type.set(type)
