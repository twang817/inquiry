from prompt_toolkit.application import Application
from prompt_toolkit.buffer import (
    AcceptAction,
    Buffer,
)
from prompt_toolkit.key_binding.defaults import load_key_bindings_for_prompt
from prompt_toolkit.styles import style_from_dict
from prompt_toolkit.token import Token
from prompt_toolkit.validation import (
    ValidationError,
    Validator,
)


_default_style = style_from_dict({
    Token.Validation.Prefix: 'noinherit #ansidarkred',
    Token.Validation.Message: 'noinherit #ansilightgray',
    Token.Prompt.Prefix: 'noinherit #ansidarkgreen',
    Token.Prompt.Message: 'noinherit #ansiwhite',
    Token.Prompt.Suffix: 'noinherit #ansilightgray',
    Token.Prompt.Transformed: 'noinherit #ansiteal',
    Token.Hidden: 'noinherit bg:#cacaca #000000',
})

class Acceptor(AcceptAction):
    def __init__(self, default, filter):
        self.default = default
        if filter is None:
            filter = lambda x: x
        self.filter = filter
        super(Acceptor, self).__init__(self.handler)
    def validate_and_handle(self, cli, buffer):
        if self.default is not None:
            if len(buffer.text) == 0:
                buffer.text = self.default
        return super(Acceptor, self).validate_and_handle(cli, buffer)
    def handler(self, cli, buffer):
        cli.set_return_value(self.filter(buffer.text))
        def reset_this_buffer():
            buffer.reset()
        cli.pre_run_callables.append(reset_this_buffer)

def create_prompt_application(layout, default=None, filter=None, validator=None, style=None):
    assert validator is None or callable(validator) or isinstance(validator, Validator)
    assert style is None or isinstance(style, Mapping)

    _validator = validator
    if not (_validator is None or isinstance(_validator, Validator)):
        class _Validator(Validator):
            def validate(self, document):
                try:
                    message = validator(document.text)
                except ValidationError:
                    raise
                except Exception as e:
                    raise ValidationError(message=e.message, cursor_position=len(document.text))
                else:
                    if message is not True:
                        if message is False:
                            message = 'invalid input'
                        raise ValidationError(message=message, cursor_position=len(document.text))
        _validator = _Validator()

    return Application(
        layout=layout,
        buffer=Buffer(
            accept_action=Acceptor(default, filter),
            validator=_validator,
        ),
        style=style or _default_style,
        key_bindings_registry=load_key_bindings_for_prompt(
            enable_system_bindings=False,
            enable_open_in_editor=False,
        ),
    )
