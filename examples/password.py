import inquiry
import json
import re


def requireLetterAndNumber(value):
    if re.search('\w', value) and re.search('\d', value):
        return True
    return 'Password need to have at least a letter and a number'

try:
    result = inquiry.prompt([
        {
            'type': 'password',
            'message': 'Enter a password',
            'name': 'password1',
            'validate': requireLetterAndNumber
        },
        {
            'type': 'password',
            'message': 'Enter a masked password',
            'name': 'password2',
            'mask': '*',
            'validate': requireLetterAndNumber
        }
    ])
except KeyboardInterrupt:
    print 'Aborted.'
else:
    print json.dumps(result, indent=2)
