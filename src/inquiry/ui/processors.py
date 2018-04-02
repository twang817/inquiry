from prompt_toolkit.layout.processors import (
    Processor,
    Transformation,
)
from prompt_toolkit.layout.utils import token_list_len
from prompt_toolkit.token import Token


class TransformProcessor(Processor):
    def __init__(self, transformer=None):
        if transformer is None:
            transformer = lambda x: x
        self.transformer = transformer
    def apply_transformation(self, cli, document, lineno, source_to_display, tokens):
        transformed = []
        for token, text in tokens:
            token = Token.Prompt.Transformed
            text = self.transformer(text)
            if isinstance(text, (list, tuple)):
                token, text = text
            transformed.append((token, text))
        return Transformation(transformed)

class HintProcessor(Processor):
    def __init__(self, hint):
        self.hint = hint
    def apply_transformation(self, cli, document, lineno, source_to_display, tokens):
        if callable(self.hint):
            before = self.hint(cli)
        else:
            before = [
                (Token.Prompt.Hint, '%s' % self.hint),
                (Token.Space, ' '),
            ]
        shift_position = token_list_len(before)
        return Transformation(
            tokens=before + tokens,
            source_to_display=lambda i: i + shift_position,
            display_to_source=lambda i: i - shift_position,
        )

class PasswordProcessor(Processor):
    def __init__(self, mask=None):
        self.mask = mask
    def apply_transformation(self, cli, document, lineno, source_to_display, tokens):
        if self.mask is not None:
            tokens = [(token, self.mask * len(text)) for token, text in tokens]
        else:
            tokens = [(Token.Hidden, '[input is hidden]')]
        return Transformation(tokens)
