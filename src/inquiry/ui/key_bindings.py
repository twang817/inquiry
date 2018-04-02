from __future__ import unicode_literals

from functools import partial
import string

from prompt_toolkit.key_binding.registry import (
    Registry,
    MergedRegistry,
)
from prompt_toolkit.key_binding.bindings.basic import (
    load_abort_and_exit_bindings,
    load_basic_system_bindings,
    load_mouse_bindings,
)
from prompt_toolkit.keys import Keys

from .controls import ListControl
from .utils import find_in_layout


def load_list_bindings():
    registry = Registry()
    handle = registry.add_binding

    @handle('k')
    @handle('K')
    @handle(Keys.Up)
    def _select_previous(event):
        control = list(find_in_layout(event.cli, ListControl))
        assert len(control) == 1
        control[0].previous_selection()
        event.cli.current_buffer.fresh = False

    @handle('j')
    @handle('J')
    @handle(Keys.Down)
    def _select_next(event):
        control = list(find_in_layout(event.cli, ListControl))
        assert len(control) == 1
        control[0].next_selection()
        event.cli.current_buffer.fresh = False

    for key in string.digits[1:]:
        def _select_by_num(event, num):
            control = list(find_in_layout(event.cli, ListControl))
            assert len(control) == 1
            control[0].set_selection(num)
            event.cli.current_buffer.fresh = False
        handle('%s' % key)(partial(_select_by_num, num=int(key)-1))

    @handle(Keys.Enter)
    def _accept_selection(event):
        control = list(find_in_layout(event.cli, ListControl))
        assert len(control) == 1
        choice = control[0].get_choice()
        event.cli.current_buffer.text = choice.value
        event.cli.set_return_value(choice.value)

    @handle(Keys.CPRResponse, save_before=lambda e: False)
    def _(event):
        """
        Handle incoming Cursor-Position-Request response.
        """
        # The incoming data looks like u'\x1b[35;1R'
        # Parse row/col information.
        row, _col = map(int, event.data[2:-1].split(';'))

        # Report absolute cursor position to the renderer.
        event.cli.renderer.report_absolute_cursor_row(row)

    return registry

def load_key_bindings_for_list():
    registry = MergedRegistry([
        load_abort_and_exit_bindings(),
        load_basic_system_bindings(),
        load_mouse_bindings(),
        load_list_bindings(),
    ])
    return registry
