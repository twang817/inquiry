import inquiry
import json

try:
    result = inquiry.prompt([
        {
            'type': 'list',
            'name': 'theme',
            'message': 'What do you want to do?',
            'choices': [
                'Order a pizza',
                'Make a reservation',
                inquiry.Separator(),
                'Ask for opening hours',
                {
                    'name': 'Contact support',
                    'disabled': 'Unavailable at this time'
                },
                'Talk to the receptionist'
            ]
        },
        {
            'type': 'list',
            'name': 'size',
            'message': 'What size do you need?',
            'choices': ['Jumbo', 'Large', 'Standard', 'Medium', 'Small', 'Micro'],
            'filter': lambda val: val.lower(),
        }
    ])
except KeyboardInterrupt:
    print 'Aborted.'
else:
    print json.dumps(result, indent=2)
