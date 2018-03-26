from ..ui import layouts, applications


def question(get_prompt_tokens, default=None, validate=None, mask=None):
    if mask is None:
        hint = '[hidden]'
    else:
        hint = '(%s)' % (mask * len(default)) if default else None
    if default is not None:
        default = u'%s' % default

    def transformer(x):
        if mask is None:
            return (Token.Hidden, '[hidden]')
        else:
            return '*' * len(x)

    layout = layouts.create_default_layout(
        get_prompt_tokens=get_prompt_tokens,
        hint=hint,
        transformer=transformer,
        is_password=True,
        password_mask=mask,
        hide_cursor=mask is None)

    return applications.create_prompt_application(
        layout,
        default=default,
        validator=validate)

