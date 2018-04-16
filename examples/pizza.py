import inquiry
import json
import re


def validate_telephone(value):
    valid = re.match('^([01]{1})?[-.\s]?\(?(\d{3})\)?[-.\s]?(\d{3})[-.\s]?(\d{4})\s?((?:#|ext\.?\s?|x\.?\s?){1}(?:\d+)?)?$', value)

    if valid:
        return True

    return 'Please enter a valid phone number';

def validate_float(value):
    try:
        float(value)
    except ValueError:
        return 'Please enter a number'
    else:
        return True

try:
    result = inquiry.prompt([
        {
            'type': 'confirm',
            'name': 'toBeDelivered',
            'message': 'Is this for delivery?',
            'default': False
        },
        {
            'type': 'input',
            'name': 'phone',
            'message': "What's your phone number?",
            'validate': validate_telephone,
        },
        {
            'type': 'list',
            'name': 'size',
            'message': 'What size do you need?',
            'choices': ['Large', 'Medium', 'Small'],
            'filter': lambda val: val.lower(),
        },
        {
            'type': 'input',
            'name': 'quantity',
            'message': 'How many do you need?',
            'validate': validate_float,
            'filter': float
        },
        {
            'type': 'expand',
            'name': 'toppings',
            'message': 'What about the toppings?',
            'choices': [
                {
                    'key': 'p',
                    'name': 'Pepperoni and cheese',
                    'value': 'PepperoniCheese'
                },
                {
                    'key': 'a',
                    'name': 'All dressed',
                    'value': 'alldressed'
                },
                {
                    'key': 'w',
                    'name': 'Hawaiian',
                    'value': 'hawaiian'
                }
            ]
        },
        {
            'type': 'rawlist',
            'name': 'beverage',
            'message': 'You also get a free 2L beverage',
            'choices': ['Pepsi', '7up', 'Coke']
        },
        {
            'type': 'input',
            'name': 'comments',
            'message': 'Any comments on your purchase experience?',
            'default': 'Nope, all good!'
        },
        {
            'type': 'list',
            'name': 'prize',
            'message': 'For leaving a comment, you get a freebie',
            'choices': ['cake', 'fries'],
            'when': lambda answers: answers['comments'] != 'Nope, all good!',
        }
    ])
except KeyboardInterrupt:
    print 'Aborted.'
else:
    print json.dumps(result, indent=2)
