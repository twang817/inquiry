from __future__ import unicode_literals

from prompt_toolkit.filters import (
    Condition,
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
from prompt_toolkit.layout.processors import (
    ConditionalProcessor,
    Processor,
    Transformation,
)
from prompt_toolkit.layout.prompt import DefaultPrompt
from prompt_toolkit.layout.utils import token_list_len
from prompt_toolkit.shortcuts import _split_multiline_prompt
from prompt_toolkit.token import Token


def _get_default_error_tokens(cli):
    buffer = cli.current_buffer
    if buffer.validation_error:
        assert len(buffer.validation_error.message) != 0
        return [
            (Token.Validation.Prefix, '>>'),
            (Token.Space, ' '),
            (Token.Validation.Message, buffer.validation_error.message),
        ]
    return []

class Transformed(Processor):
    def __init__(self, transformer=None):
        if transformer is None:
            transformer = lambda x: x
        self.transformer = transformer
    def apply_transformation(self, cli, document, lineno, source_to_display, tokens):
        transformed = []
        for token, text in tokens:
            token = Token.Prompt.Transformed
            text = self.transformer(text)
            if isinstance(text, (list, tuple)):
                token, text = text
            transformed.append((token, text))
        return Transformation(transformed)

class Hint(Processor):
    def __init__(self, hint):
        self.hint = hint
    def apply_transformation(self, cli, document, lineno, source_to_display, tokens):
        token = Token.Prompt.Hint
        if isinstance(self.hint, (tuple, list)):
            token, hint = self.hint
        else:
            hint = self.hint
        before = [
            (token, '%s' % hint),
            (Token.Space, ' '),
        ]
        shift_position = token_list_len(before)
        return Transformation(
            tokens=before + tokens,
            source_to_display=lambda i: i + shift_position,
            display_to_source=lambda i: i - shift_position,
        )

class Password(Processor):
    def __init__(self, mask=None):
        self.mask = mask
    def apply_transformation(self, cli, document, lineno, source_to_display, tokens):
        if self.mask is not None:
            tokens = [(token, self.mask * len(text)) for token, text in tokens]
        else:
            tokens = [(Token.Hidden, '[input is hidden]')]
        return Transformation(tokens)

def create_default_layout(message='', get_prompt_tokens=None, get_error_tokens=None, hint=None, transformer=None, is_password=False, password_mask=None, hide_cursor=False):
    has_before_tokens, get_prompt_tokens_1, get_prompt_tokens_2 = _split_multiline_prompt(get_prompt_tokens)
    assert get_prompt_tokens is None or callable(get_prompt_tokens)
    assert get_error_tokens is None or callable(get_error_tokens)
    assert not (message and get_prompt_tokens)

    if get_prompt_tokens is None:
        get_prompt_tokens = lambda _: [(Token.Prompt.Prefix, '?'), (Token.Space, ' '), (Token.Prompt.Message, message), (Token.Prompt.Space, ' ')]

    has_hint = to_cli_filter(hint is not None)
    IsPassword = to_cli_filter(is_password)

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
                input_processors=[
                    ConditionalProcessor(Transformed(transformer), IsDone()),
                    ConditionalProcessor(Password(password_mask), IsPassword & ~IsDone()),
                    ConditionalProcessor(Hint(hint), has_hint & ~IsDone()),
                    DefaultPrompt(get_prompt_tokens_2),
                ],
            ),
            always_hide_cursor=hide_cursor,
            dont_extend_height=True,
            wrap_lines=True,
        ),
        # ConditionalContainer(
            # Window(
                # TokenListControl(get_list_tokens),
                # dont_extend_height=True,
            # ),
            # filter=IsList() & ~IsDone()
        # ),
        ConditionalContainer(
            Window(
                TokenListControl(get_error_tokens or _get_default_error_tokens),
                dont_extend_height=True,
            ),
            filter=HasValidationError() & ~IsDone()
        ),
    ])
