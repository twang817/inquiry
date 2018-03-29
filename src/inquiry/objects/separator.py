from __future__ import unicode_literals

from .choice import Choice


class Separator(Choice):
    def __init__(self):
        super(Separator, self).__init__('-separator-', disabled=True)

    @property
    def name(self):
        return '\u2015' * 15
