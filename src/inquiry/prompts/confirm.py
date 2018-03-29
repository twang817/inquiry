from __future__ import unicode_literals

from ..ui import layouts, applications


def question(get_prompt_tokens, default=True, history=None):
    hint = '(Y/n)' if default else '(y/N)'
    default = 'Yes' if default else 'No'
    yes = ('yes', 'y')
    transformer = lambda x: 'Yes' if x.lower() in yes else 'No'
    accept_filter = lambda x: True if x.lower() in yes else False

    layout = layouts.create_default_layout(
        get_prompt_tokens=get_prompt_tokens,
        hint=hint,
        transformer=transformer)

    # don't add confirm responses to history
    history = None

    return applications.create_prompt_application(
        layout,
        default=default,
        accept_filter=accept_filter,
        history=history)
