"""Velocity Profile class."""
from subsystems.Subsystem import Subsystem
from widgets.Table import Table
from quantiphy import Quantity
import numpy as np


class VelocityProfile(Subsystem):
    """Velocity Profile Class."""

    def __init__(self, data):
        """Initialize the Class."""
        self.data = data
        self.fuel_flow = np.array([0.10, 0.50, 1.00, 5.00, 10.00, 50.00, 100.00, 500.00])

    def make_entry(self, frame):
        """Makes an entry frame."""
        self.entry = None

    def make_display(self, frame):
        """Makes a Table for data display."""
        data = ('Fuel Flow', 'Exhaust Velocity', 'ISP', 'Thrust', 'Δv', 'Acceleration', 'TWR')
        self.data_display = Table(frame, data)

    def calculate(self):
        """Do the calculations."""
        thruster_power = self.data.thruster_data["Power"]
        exhaust_velocity = np.sqrt(thruster_power / self.fuel_flow)
        isp = exhaust_velocity / 9.81
        thrust = exhaust_velocity * self.fuel_flow
        delta_v = exhaust_velocity * np.log(self.data.thruster_data["Mass Ratio"])
        acceleration = thrust / self.data.thruster_data["Mass"]
        twr = acceleration / 9.81
        self.data_display.clear()
        for idx in np.ndenumerate(self.fuel_flow):
            index = idx[0]
            data = (Quantity(self.fuel_flow[index], 'kg/s'),
                    Quantity(exhaust_velocity[index], 'm/s'),
                    Quantity(isp[index], 's'),
                    Quantity(thrust[index], 'N'),
                    Quantity(delta_v[index], 'm/s'),
                    Quantity(acceleration[index], 'm/s²'),
                    twr[index]
                    )
            self.data_display.insert(data)
