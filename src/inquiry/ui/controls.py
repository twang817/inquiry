from __future__ import unicode_literals

import collections

from prompt_toolkit.buffer import (
    AcceptAction,
    Buffer,
    ValidationState,
)
from prompt_toolkit.layout.controls import TokenListControl
from prompt_toolkit.token import Token
from prompt_toolkit.validation import (
    ValidationError,
    Validator,
)
import six

from ..objects import Choice
from .utils import if_mousedown


def make_validator(validator):
    if not (validator is None or isinstance(validator, Validator)):
        class _Validator(Validator):
            def validate(self, result):
                try:
                    message = validator(result)
                except ValidationError:
                    raise
                except Exception as ex:
                    raise ValidationError(message=ex.message)
                else:
                    if message is not True:
                        if message is False:
                            message = 'invalid choice'
                        raise ValidationError(message=message)
        return _Validator()
    return validator


class ListBuffer(Buffer):
    def __init__(self, choices, default=None, validator=None):
        self._cursor = None # not to be confused with Buffer's cursor_position
        self.init_choices(choices or [])
        self.default = default
        self.fresh = True
        self.validation_error = None
        self.validation_state = ValidationState.UNKNOWN
        super(ListBuffer, self).__init__(
            accept_action=AcceptAction(self.accept_handler),
            validator=make_validator(validator)
        )

    @property
    def cursor(self):
        return self._cursor

    @cursor.setter
    def cursor(self, value):
        if value is not None:
            assert isinstance(value, int)
            assert value < len(self.choices)
        if self._cursor != value:
            self._cursor = value
            self._input_changed()

    def _input_changed(self):
        self._cursor_position_changed()
        self.fresh = False

    def init_choices(self, choices):
        self.choices = []
        for choice in choices:
            if isinstance(choice, six.string_types):
                choice = Choice(choice)
            elif isinstance(choice, collections.Mapping):
                choice = Choice(**choice)
            assert isinstance(choice, Choice)
            self.choices.append(choice)

    def find_choice(self, value):
        first = None
        for index, choice in enumerate(self.choices):
            if choice.disabled:
                continue
            if first is None:
                first = index
            if isinstance(value, six.integer_types):
                if index == value:
                    return True, index, choice
            elif choice.value == value:
                return True, index, choice
        return False, first, self.choices[first]

    def init_default(self, default):
        self.cursor = self.find_choice(default)[1]

    def reset(self, initial_document=None, append_to_history=False):
        super(ListBuffer, self).reset(initial_document, append_to_history)
        self.init_default(self.default)
        self.fresh = True

    def get_selected(self):
        return self.choices[self.cursor]

    def accept_handler(self, cli, _buf):
        choice = self.get_selected()
        self.text = choice.value
        cli.set_return_value(choice.value)
        def reset_this_buffer():
            self.reset()
        cli.pre_run_callables.append(reset_this_buffer)

    def list_cursor_up(self, count=1):
        candidates = [(index, choice) for index, choice in enumerate(self.choices) if not choice.disabled]
        for pos, (index, choice) in enumerate(candidates):
            if index == self.cursor:
                break
        else:
            pos = 0
        pos = (pos - count) % len(candidates)
        self.cursor = candidates[pos][0]

    def list_cursor_down(self, count=1):
        self.list_cursor_up(-count)

    def validate(self):
        if self.validation_state != ValidationState.UNKNOWN:
            return self.validation_state == ValidationState.VALID

        if self.validator:
            try:
                self.validator.validate(self.get_selected())
            except ValidationError as ex:
                self.validation_state = ValidationState.INVALID
                self.validation_error = ex
                return False

        self.validation_state = ValidationState.VALID
        self.validation_error = None
        return True


class CheckboxBuffer(ListBuffer):
    def __init__(self, choices, default=None, validator=None):
        default = default or []
        if not isinstance(default, (tuple, list)):
            default = [default]
        self.selected = set()
        super(CheckboxBuffer, self).__init__(
            choices,
            default=default,
            validator=validator
        )

    def init_default(self, default):
        for index, choice in enumerate(self.choices):
            if choice.checked and index not in default:
                default.append(index)
        for value in default:
            found, index, _ = self.find_choice(value)
            if found:
                self.selected.add(index)
        self.cursor = self.find_choice(None)[1]

    def get_selected(self):
        return [choice for index, choice in enumerate(self.choices) if index in self.selected]

    def accept_handler(self, cli, _buf):
        choices = self.get_selected()
        self.text = ', '.join('%s' % choice.value for choice in choices)
        cli.set_return_value([choice.value for choice in choices])
        def reset_this_buffer():
            self.reset()
        cli.pre_run_callables.append(reset_this_buffer)

    def select_all(self):
        if self.cursor in self.selected:
            self.selected.clear()
        else:
            self.selected = set(range(len(self.choices)))
        self._input_changed()

    def invert_selection(self):
        self.selected = set(index for index in range(len(self.choices)) if index not in self.selected)
        self._input_changed()

    def toggle(self, index):
        if index not in self.selected:
            self.selected.add(index)
        else:
            self.selected.remove(index)
        self._input_changed()


class RawListBuffer(ListBuffer):
    def find_choice_by_position(self, pos):
        num = 1
        first = None
        for index, choice in enumerate(self.choices):
            if choice.disabled:
                continue
            if first is None:
                first = index
            if num == pos:
                return True, index, choice
            num += 1
        return False, first, self.choices[first]

    def _text_changed(self):
        if not self.text:
            self.init_default(self.default)
        else:
            try:
                pos = int(self.text)
            except ValueError:
                self.cursor = None
            else:
                found, index, _choice = self.find_choice_by_position(pos)
                if found:
                    self.cursor = index
                else:
                    self.cursor = None
        super(RawListBuffer, self)._text_changed()

    def validate(self):
        if self.validation_state != ValidationState.UNKNOWN:
            return self.validation_state == ValidationState.VALID

        if self.cursor is None:
            self.validation_state = ValidationState.INVALID
            self.validation_error = ValidationError(message='Please enter a valid index')
            return False

        if self.validator:
            try:
                self.validator.validate(self.get_selected())
            except ValidationError as ex:
                self.validation_state = ValidationState.INVALID
                self.validation_error = ex
                return False

        self.validation_state = ValidationState.VALID
        self.validation_error = None
        return True


class ExpandBuffer(RawListBuffer):
    def __init__(self, choices, default=None, validator=None):
        self.expanded = False
        choices.append(Choice(**{
            'key': 'H',
            'name': 'Help, list all options',
        }))
        super(ExpandBuffer, self).__init__(
            choices,
            default=default,
            validator=validator
        )

    def init_default(self, default):
        found, _index, choice = self.find_choice(default)
        if found:
            self.default = choice
        else:
            self.default = None
        self.cursor = None

    def find_choice_by_key(self, key):
        first = None
        for index, choice in enumerate(self.choices):
            if choice.disabled:
                continue
            if choice.key is None:
                continue
            if first is None:
                first = index
            if choice.key.lower() == key.lower():
                return True, index, choice
        return False, first, self.choices[first]

    def _text_changed(self):
        self.cursor = None
        if self.text:
            found, index, _choice = self.find_choice_by_key(self.text)
            if found:
                self.cursor = index
        ListBuffer._text_changed(self) # pylint: disable=protected-access

    @property
    def valid_choice(self):
        return self.find_choice_by_key(self.text)[0]

    def validate(self):
        if self.validation_state != ValidationState.UNKNOWN:
            return self.validation_state == ValidationState.VALID

        if not (self.text or self.default) or self.text.lower() == 'h':
            self.expanded = True
            self.reset()
            return False

        if not self.text and self.default:
            self.text = u'%s' % self.default.key

        if not self.valid_choice:
            self.validation_state = ValidationState.INVALID
            self.validation_error = ValidationError(message='Please enter a valid command')
            return False

        if self.validator:
            try:
                self.validator.validate(self.get_selected())
            except ValidationError as ex:
                self.validation_state = ValidationState.INVALID
                self.validation_error = ex
                return False

        self.validation_state = ValidationState.VALID
        self.validation_error = None
        return True

    def accept_handler(self, cli, _buf):
        choice = self.get_selected()
        self.text = choice.name
        cli.set_return_value(choice.value)
        def reset_this_buffer():
            self.reset()
        cli.pre_run_callables.append(reset_this_buffer)


class ListControl(TokenListControl):
    def __init__(self):
        super(ListControl, self).__init__(self.get_list_tokens)

    def get_list_tokens(self, cli): # pylint: disable=no-self-use
        tokens = []
        buf = cli.current_buffer
        def _add_choice(index, choice):
            if index == buf.cursor:
                token = Token.List.Item.Selected
                tokens.extend([
                    (Token.List.Pointer, '\u276f'),
                    (Token.Space, ' '),
                    (Token.SetCursorPosition, ''),
                ])
            else:
                token = Token.List.Item
                tokens.append((Token.Space, '  '))

            @if_mousedown
            def onclick(cli, _mouse_event):
                buf.cursor = index
                buf.accept_action.validate_and_handle(cli, buf)

            tokens.append((token, '%s' % choice.name, onclick))

        for i, choice in enumerate(buf.choices):
            _add_choice(i, choice)
            if i != len(buf.choices) - 1:
                tokens.append((Token.Space, '\n'))

        return tokens


class CheckboxControl(ListControl):
    def get_list_tokens(self, cli): # pylint: disable=no-self-use
        tokens = []
        buf = cli.current_buffer
        def _add_choice(index, choice):
            choice_tokens = [Token.Checkbox.Icon, Token.Checkbox.Item]

            if choice.disabled:
                icon = ''
            elif index in buf.selected:
                choice_tokens[0] = Token.Checkbox.Icon.Selected
                icon = '\u25c9 '
            else:
                icon = '\u25ef '

            if index == buf.cursor:
                choice_tokens[1] = Token.Checkbox.Item.Selected
                tokens.extend([
                    (Token.Checkbox.Pointer, '\u276f'),
                    (Token.Space, ' '),
                    (Token.SetCursorPosition, ''),
                ])
            else:
                tokens.append((Token.Space, '  '))

            @if_mousedown
            def onclick(_cli, _mouse_event):
                buf.toggle(index)

            tokens.extend(zip(choice_tokens, (icon, '%s' % choice.name), (onclick, onclick)))

        for i, choice in enumerate(buf.choices):
            _add_choice(i, choice)
            if i != len(buf.choices) - 1:
                tokens.append((Token.Space, '\n'))

        return tokens


class RawListControl(ListControl):
    def get_list_tokens(self, cli): # pylint: disable=no-self-use
        tokens = []
        buf = cli.current_buffer
        def _add_choice(index, num, choice):
            if index == buf.cursor:
                token = Token.List.Item.Selected
                tokens.append((Token.SetCursorPosition, ''))
            else:
                token = Token.List.Item

            @if_mousedown
            def onclick(cli, _mouse_event):
                buf.cursor = index
                buf.accept_action.validate_and_handle(cli, buf)

            tokens.append((Token.Space, '  '))

            if not choice.disabled:
                tokens.append((token, '%d)' % num))

            tokens.extend([
                (Token.Space, ' '),
                (token, '%s' % choice.name, onclick),
            ])

        num = 0
        for i, choice in enumerate(buf.choices):
            if not choice.disabled:
                num += 1
            _add_choice(i, num, choice)
            if i != len(buf.choices) - 1:
                tokens.append((Token.Space, '\n'))

        return tokens


class ExpandControl(ListControl):
    def get_list_tokens(self, cli): # pylint: disable=no-self-use
        tokens = []
        buf = cli.current_buffer
        def _add_choice(index, choice):
            if index == buf.cursor:
                token = Token.List.Item.Selected
                tokens.append((Token.SetCursorPosition, ''))
            else:
                token = Token.List.Item

            @if_mousedown
            def onclick(cli, _mouse_event):
                buf.text = u'%s' % choice.key
                buf.cursor = index
                buf.accept_action.validate_and_handle(cli, buf)

            tokens.append((Token.Space, '  '))

            if not choice.disabled:
                tokens.append((token, '%s)' % choice.key.lower()))

            tokens.extend([
                (Token.Space, ' '),
                (token, '%s' % choice.name, onclick),
            ])

        for i, choice in enumerate(buf.choices):
            _add_choice(i, choice)
            if i != len(buf.choices) - 1:
                tokens.append((Token.Space, '\n'))

        return tokens
