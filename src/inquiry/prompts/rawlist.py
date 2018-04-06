from __future__ import unicode_literals

from prompt_toolkit.layout.containers import Window
from prompt_toolkit.layout.controls import BufferControl
from prompt_toolkit.filters import IsDone
from prompt_toolkit.layout.processors import ConditionalProcessor
from prompt_toolkit.layout.prompt import DefaultPrompt
from prompt_toolkit.token import Token

from ..ui.applications import create_prompt_application
from ..ui.containers import InfiniteWindow
from ..ui.controls import (
    RawListBuffer,
    RawListControl,
)
from ..ui.layouts import create_default_layout
from ..ui.processors import HideInputProcessor
from ..ui.utils import if_mousedown


def question(get_prompt_tokens, choices, default=None, page_size=None, history=None, mouse_support=True):
    def _get_answer_tokens(_cli):
        return [
            (Token.Space, '  '),
            (Token, 'Answer:'),
            (Token.Space, ' '),
        ]

    layout = create_default_layout(
        get_prompt_tokens=get_prompt_tokens,
        extra_input_processors=[
            ConditionalProcessor(HideInputProcessor(), ~IsDone()),
        ],
        reactive_window_class=InfiniteWindow,
        reactive_control=RawListControl(),
        reactive_page_size=page_size,
        additional_reactive_windows=[
            Window(
                BufferControl(
                    input_processors=[
                        DefaultPrompt(_get_answer_tokens)
                    ],
                ),
                dont_extend_height=True,
                wrap_lines=True,
            ),
        ],
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
