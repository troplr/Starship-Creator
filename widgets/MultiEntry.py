"""MultiEntry class."""
from tkinter import Entry, Label, LabelFrame, Spinbox
from tkinter.ttk import Combobox


class MultiEntry():
    """MultiEntry class.

    This Class Creates a LabelFrame with a variable count of Labeled Widgets
    containing any Entry Widget.

    Attributes:
    root :
        The root frame where the Multi Entry Widget gets displayed
    title : str
        The Title of the LabelFrame used to contain the Entries
    entries : dict
        This data structure contains an arbritrary number of entries with
        the following structure:

        entry = {
            "Label 1": {
                "value": foo,
                "unit": "kg"
            },
            "Label 2": {
                "value": bar,
                "unit": "W",
                "type": "Spinbox",
                "config": {
                    "from": 1,
                    "to": 10,
                    "increment": 2,
                    "vaules": (1,2,4,8)
                }
            },
            "Label 3": {
                "value": baz,
                "unit": "",
                "type": "Combobox",
                "list": ["foo", "bar", "baz"]
            }
        }
    """

    def __init__(self, root, title, entries):
        """Initiates the MultiEntry."""
        self.frame = LabelFrame(root, text=title, padx=4, pady=4)
        x = 0
        for key, value in entries.items():
            Label(self.frame, text=key).grid(column=0, row=x, sticky='w', padx=2)
            if "type" in value:
                if value["type"] == "Spinbox":
                    entryfield = self.__spinbox(value["value"], value["config"])
                if value["type"] == "Combobox":
                    entryfield = self.__combobox(value["value"], value["list"])
            else:
                entryfield = self.__entry(value["value"])
            entryfield.grid(column=1, row=x, sticky='e', padx=2)
            Label(self.frame, text=value["unit"]).grid(column=2, row=x, sticky='w')
            x = x + 1
        self.frame.columnconfigure(0, weight=2)
        self.frame.columnconfigure(1, weight=1)

    def __entry(self, value):
        """Creates an Entry Widget."""
        return Entry(self.frame, textvariable=value, justify='right')

    def __spinbox(self, value, config):
        """Creates a Spinbox."""
        begin = 0
        end = 0
        increment = 1
        values = ()
        if "from" in config:
            begin = config["from"]
        if "to" in config:
            end = config["to"]
        if "increment" in config:
            increment = config["increment"]
        if "values" in config:
            values = config["values"]
        if begin:
            return Spinbox(self.frame, textvariable=value, from_=begin, to=end, increment=increment)
        if list:
            return Spinbox(self.frame, textvariable=value, values=values)

    def __combobox(self, value, values):
        """Creates a Combobox."""
        return Combobox(self.frame, textvariable=value, values=values)
