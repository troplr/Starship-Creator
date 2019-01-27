"""Display Tables."""
from tkinter.ttk import Treeview


class Table():
    """Displays Tables."""

    def __init__(self, root, columns):
        """Initialites class."""
        frame = Treeview(root)
        frame['columns'] = columns
        frame.heading('#0', anchor="w")
        frame.column('#0', width=10)
        for column in columns:
            frame.heading(column, text=column, anchor="center")
            frame.column(column, anchor="e", width=125)
        frame.grid(sticky="news")
        self.frame = frame

    def insert(self, data):
        """Adds rows."""
        self.frame.insert('', 'end', values=data)

    def clear(self):
        """Clears the Table."""
        self.frame.delete(*self.frame.get_children())
