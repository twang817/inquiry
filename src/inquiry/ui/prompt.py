from __future__ import print_function

from collections import Mapping

from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.shortcuts import run_application
from prompt_toolkit.token import Token

from .. import prompts


# avoids the cell-var-from-loop warning in pylint
def get_prompt_tokens_factory(tokens):
    def get_prompt_tokens(_cli):
        return tokens
    return get_prompt_tokens

class Prompt(object):
    def __init__(self):
        self.restoreDefaultPrompts()

    def restoreDefaultPrompts(self): # pylint: disable=invalid-name
        self.prompts = {k: getattr(prompts, k) for k in prompts.__all__}

    def registerPrompt(self, name, prompt): # pylint: disable=invalid-name
        self.prompts[name] = prompt

    def __call__(self, questions, **kwargs):
        if isinstance(questions, Mapping):
            questions = [questions]
        answers = {}

        # specific to prompt_toolkit
        run_kw = 'patch_stdout return_asyncio_coroutine true_color refresh_interval eventloop'.split()
        run_kw = {k: kwargs.pop(k) for k in run_kw if k in kwargs}
        run_kw.setdefault('true_color', True)

        history = InMemoryHistory()

        for question in questions:
            kw = {}
            kw.update(kwargs)
            kw.update(question)

            # get question type
            _type = kw.pop('type', 'input')

            # get question name
            name = kw.pop('name')

            # handle the prompt
            message = kw.pop('message')
            if callable(message):
                message = message(answers)
            tokens = [
                (Token.Prompt.Prefix, kw.pop('prefix', '?')),
                (Token.Space, ' '),
                (Token.Prompt.Message, message),
                (Token.Prompt.Suffix, kw.pop('suffix', '')),
                (Token.Space, ' '),
            ]
            kw['get_prompt_tokens'] = get_prompt_tokens_factory(tokens)

            # handle defaults
            if callable(kw.get('default', None)):
                kw['default'] = kw['default'](answers)

            # handle choices
            if callable(kw.get('choices', None)):
                kw['choices'] = kw['choices'](answers)

            # get the filter
            _filter = kw.pop('filter', None)

            # decide whether or not to ask the question
            if 'when' in kw:
                when = kw.pop('when')
                if callable(when) and not when(answers):
                    continue
                elif not when:
                    continue

            # ask the question
            kw['history'] = history

            # fix pylint warning
            kw['page_size'] = kw.pop('pageSize', None)

            application = getattr(prompts, _type).question(**kw)
            answer = run_application(application, **run_kw)

            # filter the response
            if _filter:
                answer = _filter(answer)

            # save the response to answers
            temp = answers
            path = name.split('.')
            for part in path[:-1]:
                temp = temp.setdefault(part, {})
            temp[path[-1]] = answer

        return answers
