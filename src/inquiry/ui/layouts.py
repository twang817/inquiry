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
from prompt_toolkit.layout.processors import ConditionalProcessor
from prompt_toolkit.layout.prompt import DefaultPrompt
from prompt_toolkit.shortcuts import _split_multiline_prompt
from prompt_toolkit.token import Token

from .controls import ListControl
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

class BufferFresh(Filter):
    def __call__(self, cli):
        return not hasattr(cli.current_buffer, 'fresh') or cli.current_buffer.fresh is True
    def __repr__(self):
        return 'BufferFresh()'

def create_default_layout(get_prompt_tokens, get_error_tokens=None, extra_input_processors=None, hide_cursor=False,
                          hint=None, extra_hint_filter=None, choices=None, transformer=None):
    has_before_tokens, get_prompt_tokens_1, get_prompt_tokens_2 = _split_multiline_prompt(get_prompt_tokens)
    assert get_prompt_tokens is None or callable(get_prompt_tokens)
    assert get_error_tokens is None or callable(get_error_tokens)

    has_hint = to_cli_filter(hint is not None)
    is_list = to_cli_filter(choices is not None)

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
            Window(
                ListControl(choices),
                dont_extend_height=True,
            ),
            filter=is_list & ~IsDone(),
        ),
        ConditionalContainer(
            Window(
                TokenListControl(get_error_tokens or _get_default_error_tokens),
                dont_extend_height=True,
            ),
            filter=HasValidationError() & ~IsDone(),
        ),
    ])
