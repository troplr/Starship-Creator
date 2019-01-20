"""Module to collect all Fixed Data."""

import json


class Data():
    """Loads and contains all Fixed Data."""

    def __init__(self):
        """Loads all Data."""
        self.__load_data()
        self.power_lifesupport = 0
        self.power_weapons = 0
        self.power_aux_thrusters = 0

    def __load_data(self):
        with open('data.json', "r") as data:
            json_data = json.load(data)
        self.radiators = json_data["Radiators"]
        self.life_support = json_data["Life Support"]
        self.propulsion = json_data["Propulsion"]
        self.powergeneration = json_data["Power Generation"]
        self.aux_thrusters = json_data["Auxiliary Thrusters"]
        self.main_frame = None
        self.masses = {}
        self.power = {}
        self.wasteheat = {}
        self.volumes = {}
