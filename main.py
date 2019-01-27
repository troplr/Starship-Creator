#!/usr/bin/env python3
"""
Main Script to execute the SpaceShip Creator based on my spreadsheet.
"""
# ==================
# imports
# ==================
import tkinter as tk
from tkinter import Button
from tkinter.ttk import Notebook
from Spacecraft import Spacecraft
from Data import Data


def main():
    """Main function of the program."""
    main = tk.Tk()

    # Add Title
    main.title("Space Craft Creator")

    # Disable Resizing
    main.resizable(False, False)

    data = Data()

    spacecraft = Spacecraft(data)

    notebook = Notebook(main)

    spacecraft_tab = spacecraft.make_tab(notebook)

    notebook.add(spacecraft_tab, text="Spacecraft")
    for key, subsystem in spacecraft.subsections.items():
        notebook.add(subsystem.make_tab(notebook), text=key)
    notebook.add(spacecraft.sizes.make_tab(notebook), text="Sizes")
    notebook.add(spacecraft.velocities.make_tab(notebook), text="Velocity Profiles")

    notebook.grid(column=0, row=0)
    notebook.enable_traversal()

    button = Button(main, text="Caclulate", command=spacecraft.calculate)
    button.grid(column=0, row=1)

    main.mainloop()


if __name__ == "__main__":
    main()
