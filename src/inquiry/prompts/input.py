from ..ui import layouts, applications


def question(get_prompt_tokens, default=None, validate=None, transformer=None):
    hint = '(%s)' % default if default else None
    if default is not None:
        default = u'%s' % default

    layout = layouts.create_default_layout(
        get_prompt_tokens=get_prompt_tokens,
        hint=hint,
        transformer=transformer)

    return applications.create_prompt_application(
        layout,
        default=default,
        validator=validate)
