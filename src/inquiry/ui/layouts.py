from __future__ import unicode_literals

from prompt_toolkit.filters import (
    Condition,
    Filter,
    HasValidationError,
    IsDone,
    to_cli_filter,
)
from prompt_toolkit.layout.containers import (
    ConditionalContainer,
    HSplit,
    Window,
)
from prompt_toolkit.layout.controls import (
    BufferControl,
    TokenListControl,
)
from prompt_toolkit.layout.dimension import LayoutDimension
from prompt_toolkit.layout.processors import ConditionalProcessor
from prompt_toolkit.layout.prompt import DefaultPrompt
from prompt_toolkit.shortcuts import _split_multiline_prompt
from prompt_toolkit.token import Token

from .processors import (
    TransformProcessor,
    HintProcessor,
)


def _get_default_error_tokens(cli):
    buf = cli.current_buffer
    if buf.validation_error:
        assert buf.validation_error.message
        return [
            (Token.Validation.Prefix, '>>'),
            (Token.Space, ' '),
            (Token.Validation.Message, buf.validation_error.message),
        ]
    return []

def _get_default_pager_tokens(_cli):
    return [
        (Token, '(Move up and down to reveal more choices)')
    ]

def _get_default_answer_tokens(_cli):
    return [
        (Token, '  Answer: '),
    ]

class BufferFresh(Filter):
    def __call__(self, cli):
        return not hasattr(cli.current_buffer, 'fresh') or cli.current_buffer.fresh is True

    def __repr__(self):
        return 'BufferFresh()'

class NeedsScrollTip(Filter):
    def __init__(self, page_size):
        self.page_size = page_size

    def __call__(self, cli):
        return len(cli.current_buffer.choices) > self.page_size

def list_window_factory(window_class, control, page_size):
    page_size = page_size or 7
    def _factory():
        return [
            window_class(
                control,
                height=LayoutDimension(max=page_size),
                dont_extend_height=True,
                wrap_lines=True,
            ),
            ConditionalContainer(
                Window(
                    TokenListControl(_get_default_pager_tokens),
                    dont_extend_height=True,
                    wrap_lines=True,
                ),
                filter=NeedsScrollTip(page_size) & ~IsDone(),
            ),
        ]
    return _factory

def rawlist_window_factory(window_class, control, page_size):
    def _factory():
        return list_window_factory(window_class, control, page_size)() + [
            Window(
                BufferControl(
                    input_processors=[
                        DefaultPrompt(_get_default_answer_tokens)
                    ],
                ),
                dont_extend_height=True,
                wrap_lines=True,
            )
        ]
    return _factory

def create_default_layout(get_prompt_tokens, get_error_tokens=None, extra_input_processors=None, hide_cursor=False,
                          hint=None, extra_hint_filter=None, reactive_window_factory=None, transformer=None):
    has_before_tokens, get_prompt_tokens_1, get_prompt_tokens_2 = _split_multiline_prompt(get_prompt_tokens)

    assert get_prompt_tokens is None or callable(get_prompt_tokens)
    assert get_error_tokens is None or callable(get_error_tokens)

    reactive_windows = []
    if callable(reactive_window_factory):
        reactive_windows = reactive_window_factory()
    has_reactive = to_cli_filter(reactive_windows is not None)

    has_hint = to_cli_filter(hint is not None)

    hint_filter = has_hint
    if extra_hint_filter is not None:
        hint_filter = hint_filter & extra_hint_filter

    input_processors = []
    if extra_input_processors is not None:
        input_processors.extend(extra_input_processors)

    input_processors.extend([
        ConditionalProcessor(HintProcessor(hint), hint_filter & ~IsDone()),
        ConditionalProcessor(TransformProcessor(transformer), IsDone()),
        DefaultPrompt(get_prompt_tokens_2),
    ])

    return HSplit([
        ConditionalContainer(
            Window(
                TokenListControl(get_prompt_tokens_1),
                dont_extend_height=True,
                wrap_lines=True,
            ),
            Condition(has_before_tokens),
        ),
        Window(
            BufferControl(
                input_processors=input_processors,
            ),
            always_hide_cursor=hide_cursor,
            dont_extend_height=True,
            wrap_lines=True,
        ),
        ConditionalContainer(
            HSplit(reactive_windows),
            filter=has_reactive & ~IsDone(),
        ),
        ConditionalContainer(
            Window(
                TokenListControl(get_error_tokens or _get_default_error_tokens),
                dont_extend_height=True,
                wrap_lines=True,
            ),
            filter=HasValidationError() & ~IsDone(),
        ),
    ])
