from tkinter import Entry, Label, LabelFrame


class MultiEntry():
    """
    This Class Creates a LabelFrame with a variable count of Labeled Entry Widgets
    """

    def __init__(self, root, title, entries):
        """
        Initiates the MultiEntry
        """
        self.frame = LabelFrame(root, text=title, padx=4, pady=4)
        x = 0
        for key, value in entries.items():
            Label(self.frame, text=key).grid(column=0, row=x, sticky='w', padx=2)
            Entry(self.frame, textvariable=value["value"], justify='right').grid(column=1, row=x, sticky='e', padx=2)
            Label(self.frame, text=value["unit"]).grid(column=2, row=x, sticky='w')
            x = x + 1
        self.frame.columnconfigure(0, weight=2)
        self.frame.columnconfigure(1, weight=1)
