import inquiry
import json

try:
    result = inquiry.prompt([
        {
            'type': 'expand',
            'message': 'Conflict on `file.js`: ',
            'name': 'overwrite',
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
