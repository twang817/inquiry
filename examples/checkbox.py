import inquiry
import json

result = inquiry.prompt([
    {
        'type': 'checkbox',
        'message': 'Select toppings',
        'name': 'toppings',
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
