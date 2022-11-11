"""
Customized spinbox widget which supports validation for integers.
"""

from tkinter import ttk

class Spinbox(ttk.Spinbox):
    def __init__(self, master=None, from_=None, to=None, **kw):
        ttk.Spinbox.__init__(self, master, from_=from_, to=to, **kw)
        self.from_ = from_
        self.to = to
        self._validate = self.register(self._on_validate)
        self.config(validate="key", validatecommand=(self._validate, '%P'))

    def _on_validate(self, new_value):
        if not new_value:
            return True
        try:
            new_value = int(new_value)
        except ValueError:
            return False
        if self.from_ is not None and new_value < self.from_:
            return False
        if self.to is not None and new_value > self.to:
            return False
        return True