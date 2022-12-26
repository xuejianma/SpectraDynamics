"""
Customized spinbox widget which supports validation for integers.
"""

from tkinter import ttk


class Spinbox(ttk.Spinbox):
    def __init__(self, master=None, from_=None, to=None, **kw):
        super().__init__(master, from_=from_, to=to, **kw)
        self.from_ = from_  # for typing in validating
        self.to = to  # for typing in validating
        self._validate = self.register(self._on_validate)
        self.config(validate="key", validatecommand=(self._validate, '%P'))

    def _on_validate(self, new_value):
        if not new_value:
            return True
        try:
            new_value = float(new_value)
        except ValueError:
            return False
        if self.from_ is not None and new_value < self.from_:
            return False
        if self.to is not None and new_value > self.to:
            return False
        return True
    
    def config(self, cnf=None, **kw):
        if cnf is None:
            cnf = {}
        cnf = cnf.copy()
        cnf.update(kw)
        if 'from_' in cnf:
            self.from_ = float(cnf.get('from_'))
        if 'to' in cnf:
            self.to = float(cnf.get('to'))
        super().config(cnf)
