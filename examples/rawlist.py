import inquiry
import json

try:
    result = inquiry.prompt([
        {
            'type': 'rawlist',
            'name': 'theme',
            'message': 'What do you want to do?',
            'choices': [
                'Order a pizza',
                'Make a reservation',
                inquiry.Separator(),
                'Ask opening hours',
                'Talk to the receptionist'
            ]
        },
        {
            'type': 'rawlist',
            'name': 'size',
            'message': 'What size do you need',
            'choices': ['Jumbo', 'Large', 'Standard', 'Medium', 'Small', 'Micro'],
            'filter': lambda val: val.lower(),
        }
    ])
except KeyboardInterrupt:
    print 'Aborted.'
else:
    print json.dumps(result, indent=2)
