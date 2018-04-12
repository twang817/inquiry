from __future__ import unicode_literals

import six


class Choice(object):
    def __init__(self, name, value=None, key=None, short=None, disabled=None, checked=False):
        self._name = name
        self._value = value or name
        self.key = key
        self.short = short or name
        self.disabled = bool(disabled)
        self.checked = checked
        if self.disabled:
            if isinstance(disabled, six.string_types):
                self.reason = disabled
            else:
                self.reason = 'Disabled'

    @property
    def name(self):
        if self.disabled:
            return '- %s (%s)' % (self._name, self.reason)
        return '%s' % self._name

    @property
    def value(self):
        return '%s' % self._value
