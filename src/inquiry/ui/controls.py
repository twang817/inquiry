from __future__ import unicode_literals

from collections import Mapping

from prompt_toolkit.layout.controls import TokenListControl
from prompt_toolkit.token import Token
import six

from ..objects import Choice


class ListControl(TokenListControl):
    def __init__(self, choices, default=None):
        self.selected = None
        if choices is not None:
            self.init_choices(choices)
            self.set_selection(default, fallback_first=True)
        super(ListControl, self).__init__(self.get_list_tokens)

    def init_choices(self, choices):
        self.choices = []
        index = 0
        for choice in choices:
            if isinstance(choice, six.string_types):
                choice = Choice(choice)
            elif isinstance(choice, Mapping):
                choice = Choice(**choice)
            assert isinstance(choice, Choice)
            self.choices.append(choice)
            if choice.disabled:
                continue
            choice.set_index(index)
            index += 1

    def set_selection(self, value, fallback_first=False):
        first = None
        for index, choice in enumerate(self.choices):
            if first is None and not choice.disabled:
                first = index
            if isinstance(value, six.integer_types):
                if choice.index == value:
                    self.selected = index
                    break
            elif choice.value == value:
                self.selected = index
                break
        else:
            if fallback_first:
                self.selected = first

    def next_selection(self):
        candidate = self.selected
        while True:
            candidate = (candidate + 1) % len(self.choices)
            choice = self.choices[candidate]
            if not choice.disabled:
                self.selected = candidate
                return choice
            if candidate == self.selected:
                break

    def previous_selection(self):
        candidate = self.selected
        while True:
            candidate = (candidate - 1) % len(self.choices)
            choice = self.choices[candidate]
            if not choice.disabled:
                self.selected = candidate
                return choice
            if candidate == self.selected:
                break

    def get_list_tokens(self, _cli):
        tokens = []
        for i, choice in enumerate(self.choices):
            if i == self.selected:
                token = Token.List.Item.Selected
                tokens.extend([
                    (Token.List.Pointer, '\u276f'),
                    (Token.Space, ' '),
                ])
            else:
                token = Token.List.Item
                tokens.append((Token.Space, '  '))

            tokens.append((token, choice.name))
            tokens.append((Token.Space, '\n'))
        return tokens

    def get_choice(self):
        return self.choices[self.selected]
