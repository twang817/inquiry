from __future__ import unicode_literals

from .choice import Choice


class Separator(Choice):
    def __init__(self, name=None):
        super(Separator, self).__init__(name, disabled=True)

    @property
    def name(self):
        if self._name:
            return self._name
        return '\u2015' * 15
