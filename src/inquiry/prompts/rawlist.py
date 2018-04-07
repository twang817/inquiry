from __future__ import unicode_literals

from prompt_toolkit.filters import IsDone
from prompt_toolkit.layout.processors import ConditionalProcessor

from ..ui.applications import create_prompt_application
from ..ui.containers import InfiniteWindow
from ..ui.controls import (
    RawListBuffer,
    RawListControl,
)
from ..ui.layouts import (
    create_default_layout,
    rawlist_window_factory
)
from ..ui.processors import HideInputProcessor


def question(get_prompt_tokens, choices, default=None, page_size=None, history=None, mouse_support=True):
    layout = create_default_layout(
        get_prompt_tokens=get_prompt_tokens,
        extra_input_processors=[
            ConditionalProcessor(HideInputProcessor(), ~IsDone()),
        ],
        reactive_window_factory=rawlist_window_factory(InfiniteWindow, RawListControl(), page_size),
        hide_cursor=True)

    # don't add list responses to history
    history = None

    return create_prompt_application(
        layout,
        buf=RawListBuffer(
            choices,
            default,
        ),
        history=history,
        mouse_support=mouse_support)
