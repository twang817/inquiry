import inquiry
import json
import re


def validate_telephone(value):
    valid = re.match('^([01]{1})?[-.\s]?\(?(\d{3})\)?[-.\s]?(\d{3})[-.\s]?(\d{4})\s?((?:#|ext\.?\s?|x\.?\s?){1}(?:\d+)?)?$', value)

    if valid:
        return True

    return 'Please enter a valid phone number';

try:
    result = inquiry.prompt([
        {
            'type': 'input',
            'name': 'first_name',
            'message': "What's your first name"
        },
        {
            'type': 'input',
            'name': 'last_name',
            'message': "What's your last name",
            'default': lambda answers: 'Doe',
        },
        {
            'type': 'input',
            'name': 'phone',
            'message': "What's your phone number",
            'validate': validate_telephone
        }
    ])
except KeyboardInterrupt:
    print 'Aborted.'
else:
    print json.dumps(result, indent=2)
