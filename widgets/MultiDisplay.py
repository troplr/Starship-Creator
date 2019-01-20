"""MultiDisplay class."""
from tkinter import Label, LabelFrame


class MultiDisplay():
    """Class to display multiple Variables."""

    def __init__(self, root, title):
        """Init the Class."""
        self.frame = LabelFrame(root, text=title, padx=4, pady=4)

    def make_display(self, entries):
        """Creates the Entries."""
        x = 0
        for key, value in entries.items():
            if isinstance(value["value"], MultiDisplay):
                value["value"].frame.grid(column=0, row=x, columnspan=3, sticky="we", padx=4, pady=4)
            else:
                Label(self.frame, text=key).grid(column=0, row=x, sticky="w", padx=2)
                Label(self.frame, textvariable=value["value"]).grid(column=1, row=x, sticky="e", padx=2)
                if "unit" in value:
                    Label(self.frame, text=value["unit"]).grid(column=2, row=x, sticky="w")
            x = x + 1
