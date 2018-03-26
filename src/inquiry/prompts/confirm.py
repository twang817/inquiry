from ..ui import layouts, applications


def question(get_prompt_tokens, default=True):
    hint = '(Y/n)' if default else '(y/N)'
    default = u'Yes' if default else u'No'
    yes = ('yes', 'y')
    transformer = lambda x: 'Yes' if x.lower() in yes else 'No'
    filter = lambda x: True if x.lower() in yes else False

    layout = layouts.create_default_layout(
        get_prompt_tokens=get_prompt_tokens,
        hint=hint,
        transformer=transformer)

    return applications.create_prompt_application(
        layout,
        default=default,
        filter=filter)
