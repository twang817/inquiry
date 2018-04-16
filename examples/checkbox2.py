import inquiry
import json

# example of defaults & filters in checkboxes
# Note, we differ from inquirer in that we can accept an array of the choice value OR the position of the choice.
try:
    result = inquiry.prompt([
        {
            'type': 'checkbox',
            'message': 'Select toppings',
            'name': 'toppings',
            'default': ['Ham', 3, 'Bacon'],
            'filter': lambda x: [c.upper() for c in x],
            'choices': [
                inquiry.Separator(' = The Meats = '),
                {
                    'name': 'Pepperoni'
                },
                {
                    'name': 'Ham'
                },
                {
                    'name': 'Ground Meat'
                },
                {
                    'name': 'Bacon'
                },
                inquiry.Separator(' = The Cheeses = '),
                {
                    'name': 'Mozzarella',
                    'checked': True
                },
                {
                    'name': 'Cheddar'
                },
                {
                    'name': 'Parmesan'
                },
                inquiry.Separator(' = The usual ='),
                {
                    'name': 'Mushroom'
                },
                {
                    'name': 'Tomato'
                },
                inquiry.Separator(' = The extras = '),
                {
                    'name': 'Pineapple'
                },
                {
                    'name': 'Olives',
                    'disabled': 'out of stock'
                },
                {
                    'name': 'Extra cheese'
                }
            ],
            'validate': lambda answer: 'You must choose at least one topping.' if len(answer) < 1 else True
        }
    ])
except KeyboardInterrupt:
    print 'Aborted.'
else:
    print json.dumps(result, indent=2)
