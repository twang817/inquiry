import inquiry
import json

# 1. tests default in checkbox
# Note, we differ from inquirer in that we can accept an array of the choice value OR the index of the choice
#
# 2. test filter in checkbox
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

print json.dumps(result, indent=2)
