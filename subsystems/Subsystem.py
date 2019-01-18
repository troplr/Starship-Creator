"""Subsystem Base Class."""

from math import ceil
from tkinter.ttk import Frame
from widgets.MultiEntry import MultiEntry
from widgets.MultiDisplay import MultiDisplay


class Subsystem():
    """Base Class for all Subsystems of the Spacecraft."""

    def _roundup(self, x, next_largest):
        """Rounds a number up to the next largest."""
        return float(ceil(x / next_largest)) * next_largest

    def _format_number(self, x):
        """Formats a number."""
        return "{:.2f}".format(x)

    def make_tab(self, root):
        """Creates a Tab Widgets with the Entry and Data Displays.

        Makes use of self.make_entry and self.make_display.
        """
        self.frame = Frame(root)
        self.make_entry(self.frame)
        self.make_display(self.frame)
        return self.frame

    def _make_entry(self, frame, title, entry):
        """Makes the Entry complete."""
        self.entry = MultiEntry(frame, title, entry)
        self.entry.frame.grid(column=1, row=0, sticky='new', padx=5)

    def _make_display(self, frame, title, data):
        """Makes the Display complete."""
        self.data_display = MultiDisplay(frame, title)
        self.data_display.make_display(data)
        self.data_display.frame.grid(column=1, row=1, sticky='new', padx=5)
