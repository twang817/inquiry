from __future__ import unicode_literals

from ..ui.applications import create_prompt_application
from ..ui.containers import InfiniteWindow
from ..ui.controls import (
    ListBuffer,
    ListControl,
)
from ..ui.key_bindings import load_key_bindings_for_list
from ..ui.layouts import (
    BufferFresh,
    create_default_layout,
    list_window_factory,
)


def question(get_prompt_tokens, choices, default=None, page_size=None, history=None, mouse_support=True):
    layout = create_default_layout(
        get_prompt_tokens=get_prompt_tokens,
        hint='(Use arrow keys)',
        extra_hint_filter=BufferFresh(),
        reactive_window_factory=list_window_factory(InfiniteWindow, ListControl(), page_size),
        hide_cursor=True)

    registry = load_key_bindings_for_list()

    # don't add list responses to history
    history = None

    return create_prompt_application(
        layout,
        buf=ListBuffer(
            choices,
            default,
        ),
        key_bindings_registry=registry,
        history=history,
        mouse_support=mouse_support)
