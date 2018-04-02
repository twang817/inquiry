from __future__ import unicode_literals

from prompt_toolkit.token import Token

from ..ui.applications import create_prompt_application
from ..ui.containers import InfiniteWindow
from ..ui.controls import (
    CheckboxBuffer,
    CheckboxControl,
)
from ..ui.key_bindings import load_key_bindings_for_checkbox
from ..ui.layouts import (
    create_default_layout,
    BufferFresh,
)


def question(get_prompt_tokens, choices, default=None, validate=None, page_size=None, history=None, mouse_support=True):
    def hint(_cli):
        return [
            (Token.Prompt.Hint, '(Press '),
            (Token.Prompt.Hint.Highlight, '<space>'),
            (Token.Prompt.Hint, ' to select, '),
            (Token.Prompt.Hint.Highlight, '<a>'),
            (Token.Prompt.Hint, ' to toggle all, '),
            (Token.Prompt.Hint.Highlight, '<i>'),
            (Token.Prompt.Hint, ' to invert selection)'),
        ]

    layout = create_default_layout(
        get_prompt_tokens=get_prompt_tokens,
        hint=hint,
        extra_hint_filter=BufferFresh(),
        reactive_window_class=InfiniteWindow,
        reactive_control=CheckboxControl(),
        reactive_page_size=page_size,
        hide_cursor=True)

    registry = load_key_bindings_for_checkbox()

    # don't add list responses to history
    history = None

    return create_prompt_application(
        layout,
        buf=CheckboxBuffer(
            choices,
            default,
            validate,
        ),
        key_bindings_registry=registry,
        history=history,
        mouse_support=mouse_support)
