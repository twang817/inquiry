from __future__ import unicode_literals

from ..ui import layouts, applications, key_bindings


def question(get_prompt_tokens, choices, default=None, page_size=None, history=None, mouse_support=True):
    layout = layouts.create_default_layout(
        get_prompt_tokens=get_prompt_tokens,
        hint='(use arrow keys)',
        extra_hint_filter=layouts.BufferFresh(),
        page_size=page_size,
        hide_cursor=True,
        choices=choices,
        default_choice=default)

    registry = key_bindings.load_key_bindings_for_list()

    # don't add list responses to history
    history = None

    return applications.create_prompt_application(
        layout,
        key_bindings_registry=registry,
        history=history,
        mouse_support=mouse_support)
