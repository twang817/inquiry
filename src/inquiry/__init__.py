'''
inquiry - module for Inquirer.JS like prompts
'''
from .ui.prompt import Prompt
from .objects import (
    Choice,
    Separator,
)


# pylint: disable=invalid-name
prompt = Prompt()
