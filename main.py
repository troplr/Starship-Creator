#!/usr/bin/env python3
"""
Main Script to execute the SpaceShip Creator based on my spreadsheet.
"""
# ==================
# imports
# ==================
import tkinter as tk
from tkinter import Button
from MultiEntry import MultiEntry
from Spacecraft import Spacecraft
from Data import Data


def main():
    """
    Main function of the program.
    """
    main = tk.Tk()

    # Add Title
    main.title("Space Craft Creator")

    # Disable Resizing
    main.resizable(False, False)

    data = Data()

    spacecraft = Spacecraft(data)
    masses = {
        "Armor Mass": {"value": spacecraft.mass_armor, "unit": "kg"},
        "Defensive Mass": {"value": spacecraft.mass_defensive, "unit": "kg"},
        "Cargo Mass": {"value": spacecraft.mass_cargo, "unit": "kg"},
        "Other Mass": {"value": spacecraft.mass_other, "unit": "kg"},
    }
    mass_entry = MultiEntry(main, "Masses", masses)

    power = {
        "Number of Reactors": {"value": spacecraft.no_reactors, "unit": ""},
    }
    power_entry = MultiEntry(main, "Power", power)

    spacecraft.make_entry(main)
    spacecraft.make_display(main)

    button = Button(main, text="Caclulate", command=spacecraft.calculate)
    button.grid(column=2, row=3)

    main.mainloop()


if __name__ == "__main__":
    main()
