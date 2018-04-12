from __future__ import unicode_literals

from prompt_toolkit.filters import IsDone
from prompt_toolkit.layout.processors import ConditionalProcessor

from ..ui.applications import create_prompt_application
from ..ui.containers import InfiniteWindow
from ..ui.controls import (
    ExpandBuffer,
    ExpandControl,
)
from ..ui.layouts import (
    create_default_layout,
    expand_window_factory,
    Expanded,
)
from ..ui.processors import HideInputProcessor


def question(get_prompt_tokens, choices, default=None, page_size=None, history=None, mouse_support=True):
    buf = ExpandBuffer(
        choices,
        default,
    )
    hint = []
    for choice in buf.choices:
        if choice.key:
            if choice.key not in hint:
                hint.append(choice.key)
    hint = '(%s)' % ''.join(hint)

    layout = create_default_layout(
        get_prompt_tokens=get_prompt_tokens,
        hint=hint,
        extra_input_processors=[
            ConditionalProcessor(HideInputProcessor(), ~IsDone() & Expanded()),
        ],
        reactive_window_factory=expand_window_factory(InfiniteWindow, ExpandControl(), page_size))

    # don't add list responses to history
    history = None

    return create_prompt_application(
        layout,
        buf=buf,
        history=history,
        mouse_support=mouse_support)
