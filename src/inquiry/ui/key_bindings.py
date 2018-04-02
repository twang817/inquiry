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


def load_cpr_bindings():
    registry = Registry()
    handle = registry.add_binding

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

def load_scroll_bindings():
    registry = Registry()
    handle = registry.add_binding

    @handle('k')
    @handle('K')
    @handle(Keys.Up)
    def _cursor_up(event):
        event.current_buffer.cursor_up()

    @handle('j')
    @handle('J')
    @handle(Keys.Down)
    def _cursor_down(event):
        event.current_buffer.cursor_down()

    for key in string.digits[1:]:
        def _set_cursor(event, num):
            event.current_buffer.cursor = num
        handle('%s' % key)(partial(_set_cursor, num=int(key)-1))

    return registry

def load_list_bindings():
    registry = Registry()
    handle = registry.add_binding

    @handle(Keys.Enter)
    def _accept_selection(event):
        buf = event.current_buffer
        buf.accept_action.validate_and_handle(event.cli, buf)

    return registry

def load_checkbox_bindings():
    registry = Registry()
    handle = registry.add_binding

    @handle('a')
    def _select_all(event):
        event.current_buffer.select_all()

    @handle('i')
    def _invert_selection(event):
        event.current_buffer.invert_selection()

    @handle(' ')
    def _select(event):
        buf = event.current_buffer
        buf.toggle(buf.cursor)

    @handle(Keys.Enter)
    def _accept_selection(event):
        buf = event.current_buffer
        buf.accept_action.validate_and_handle(event.cli, buf)

    return registry

def _load_key_bindings(*registries):
    registry = MergedRegistry([
        load_abort_and_exit_bindings(),
        load_basic_system_bindings(),
        load_mouse_bindings(),
        load_cpr_bindings(),
    ] + list(registries))
    return registry

def load_key_bindings_for_list():
    return _load_key_bindings(
        load_scroll_bindings(),
        load_list_bindings(),
    )

def load_key_bindings_for_checkbox():
    return _load_key_bindings(
        load_scroll_bindings(),
        load_checkbox_bindings(),
    )
