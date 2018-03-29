from __future__ import unicode_literals

from ..ui import layouts, applications


def question(get_prompt_tokens, default=None, validate=None, transformer=None, history=None):
    hint = None
    if default is not None:
        default = '%s' % default
        hint = '(%s)' % default

    layout = layouts.create_default_layout(
        get_prompt_tokens=get_prompt_tokens,
        hint=hint,
        transformer=transformer)

    return applications.create_prompt_application(
        layout,
        default=default,
        validator=validate,
        history=history)
