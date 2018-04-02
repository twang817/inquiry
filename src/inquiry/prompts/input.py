from __future__ import unicode_literals

from ..ui.applications import create_prompt_application
from ..ui.layouts import create_default_layout


def question(get_prompt_tokens, default=None, validate=None, transformer=None, history=None):
    hint = None
    if default is not None:
        default = '%s' % default
        hint = '(%s)' % default

    layout = create_default_layout(
        get_prompt_tokens=get_prompt_tokens,
        hint=hint,
        transformer=transformer)

    return create_prompt_application(
        layout,
        default=default,
        validator=validate,
        history=history)
