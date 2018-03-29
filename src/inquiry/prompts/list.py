from __future__ import unicode_literals

from ..ui import layouts, applications, key_bindings


def question(get_prompt_tokens, choices, default=None, history=None):
    if default is not None:
        default = '%s' % default

    layout = layouts.create_default_layout(
        get_prompt_tokens=get_prompt_tokens,
        hint='(use arrow keys)',
        extra_hint_filter=layouts.BufferFresh(),
        hide_cursor=True,
        choices=choices)

    registry = key_bindings.load_key_bindings_for_list()

    # don't add list responses to history
    history = None

    return applications.create_prompt_application(
        layout,
        key_bindings_registry=registry,
        history=history)
