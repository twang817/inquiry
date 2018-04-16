import inquiry
import json

# example of defaults for expand
# Note, we differ from inquirer in that we can accept the position of the choice OR the choice value
try:
    result = inquiry.prompt([
        {
            'type': 'expand',
            'message': 'Conflict on `file.js`: ',
            'name': 'overwrite',
            'default': 3,
            'choices': [
                {
                    'key': 'y',
                    'name': 'Overwrite',
                    'value': 'overwrite'
                },
                {
                    'key': 'a',
                    'name': 'Overwrite this one and all next',
                    'value': 'overwrite_all'
                },
                {
                    'key': 'd',
                    'name': 'Show diff',
                    'value': 'diff'
                },
                inquiry.Separator(),
                {
                    'key': 'x',
                    'name': 'Abort',
                    'value': 'abort'
                }
            ]
        }
    ])
except KeyboardInterrupt:
    print 'Aborted.'
else:
    print json.dumps(result, indent=2)
