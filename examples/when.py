import inquiry
import json

def likesFood(aFood):
    def f(answers):
        return answers.get(aFood, False)
    return f

try:
    result = inquiry.prompt([
        {
            'type': 'confirm',
            'name': 'bacon',
            'message': 'Do you like bacon?'
        },
        {
            'type': 'input',
            'name': 'favorite',
            'message': 'Bacon lover, what is your favorite type of bacon?',
            'when': lambda answers: answers.get('bacon', None),
        },
        {
            'type': 'confirm',
            'name': 'pizza',
            'message': 'Ok... Do you like pizza?',
            'when': lambda answers: not likesFood('bacon')(answers),
        },
        {
            'type': 'input',
            'name': 'favorite',
            'message': 'Whew! What is your favorite type of pizza?',
            'when': likesFood('pizza'),
        }
    ])
except KeyboardInterrupt:
    print 'Aborted.'
else:
    print json.dumps(result, indent=2)
