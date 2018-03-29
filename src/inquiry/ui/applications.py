from collections import Mapping

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


DEFAULT_STYLE = style_from_dict({
    Token.Validation.Prefix: 'noinherit #ansidarkred',
    Token.Validation.Message: 'noinherit #ansilightgray',
    Token.Prompt.Prefix: 'noinherit #ansidarkgreen',
    Token.Prompt.Message: 'noinherit #ansiwhite',
    Token.Prompt.Suffix: 'noinherit #ansilightgray',
    Token.Prompt.Transformed: 'noinherit #ansiteal',
    Token.Hidden: 'noinherit bg:#cacaca #000000',
    Token.List.Pointer: 'noinherit #ansiteal',
    Token.List.Item.Selected: 'noinherit #ansiteal',
})

class Acceptor(AcceptAction):
    def __init__(self, default, response_filter):
        self.default = default
        if response_filter is None:
            response_filter = lambda x: x
        def handler(cli, buf):
            cli.set_return_value(response_filter(buf.text))
            def reset_this_buffer():
                buf.reset()
            cli.pre_run_callables.append(reset_this_buffer)
        super(Acceptor, self).__init__(handler)

    def validate_and_handle(self, cli, buf):
        if self.default is not None:
            if len(buf.text) == 0: # pylint: disable=len-as-condition
                buf.text = self.default
        return super(Acceptor, self).validate_and_handle(cli, buf)

def create_prompt_application(layout, default=None, accept_filter=None, validator=None, history=None,
                              key_bindings_registry=None, style=None):
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
                except Exception as ex:
                    raise ValidationError(message=ex.message, cursor_position=len(document.text))
                else:
                    if message is not True:
                        if message is False:
                            message = 'invalid input'
                        raise ValidationError(message=message, cursor_position=len(document.text))
        _validator = _Validator()

    if key_bindings_registry is None:
        key_bindings_registry = load_key_bindings_for_prompt(
            enable_search=False,
            enable_auto_suggest_bindings=False,
            enable_system_bindings=True,
        )

    buf = Buffer(
        accept_action=Acceptor(default, accept_filter),
        validator=_validator,
        history=history,
    )

    if style is not None:
        style = style_from_dict(style)

    return Application(
        layout=layout,
        buffer=buf,
        style=style or DEFAULT_STYLE,
        key_bindings_registry=key_bindings_registry,
    )
