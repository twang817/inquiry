from __future__ import unicode_literals

from prompt_toolkit.filters import IsDone
from prompt_toolkit.layout.processors import ConditionalProcessor
from prompt_toolkit.token import Token

from ..ui.applications import create_prompt_application
from ..ui.layouts import create_default_layout
from ..ui.processors import PasswordProcessor


def question(get_prompt_tokens, default=None, validate=None, mask=None, history=None):
    hint = None
    if default is not None:
        default = '%s' % default
        if mask is None:
            hint = '[hidden]'
        else:
            hint = '(%s)' % (mask * len(default))

    def transformer(text):
        if mask is None:
            return (Token.Hidden, '[hidden]')
        return '*' * len(text)

    layout = create_default_layout(
        get_prompt_tokens=get_prompt_tokens,
        hint=hint,
        transformer=transformer,
        extra_input_processors=[
            ConditionalProcessor(PasswordProcessor(mask), ~IsDone()),
        ],
        hide_cursor=mask is None)

    # don't add password responses to history
    history = None

    return create_prompt_application(
        layout,
        default=default,
        validator=validate,
        history=history)
