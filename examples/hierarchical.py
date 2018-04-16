import inquiry
import json

directionsPrompt = {
    'type': 'list',
    'name': 'direction',
    'message': 'Which direction would you like to go?',
    'choices': ['Forward', 'Right', 'Left', 'Back']
};

def main():
    print 'You find youself in a small room, there is a door in front of you.'
    exitHouse()

def exitHouse():
    answers = inquiry.prompt(directionsPrompt)
    if answers['direction'] == 'Forward':
        print 'You find yourself in a forest'
        print 'There is a wolf in front of you; a friendly looking dwarf to the right and an impasse to the left.'
        encounter1()
    else:
        print 'You cannot go that way. Try again'
        exitHouse();

def encounter1():
    answers = inquiry.prompt(directionsPrompt)
    direction = answers['direction']
    if direction == 'Forward':
        print 'You attempt to fight the wolf'
        print 'Theres a stick and some stones lying around you could use as a weapon'
        encounter2b()
    elif direction == 'Right':
        print 'You befriend the dwarf'
        print 'He helps you kill the wolf. You can now move forward'
        encounter2a()
    else:
        print 'You cannot go that way'
        encounter1()

def encounter2a():
    answers = inquiry.prompt(directionsPrompt)
    direction = answers['direction']
    if direction == 'Forward':
        print 'You find a painted wooden sign that says:'
        print ' ____  _____  ____  _____ '
        print '(_  _)(  _  )(  _ \\(  _  ) '
        print '  )(   )(_)(  )(_) ))(_)(  '
        print ' (__) (_____)(____/(_____) '
    else:
        print 'You cannot go that way'
        encounter2a()

def encounter2b():
    inquiry.prompt({
        'type': 'list',
        'name': 'weapon',
        'message': 'Pick one',
        'choices': [
            'Use the stick',
            'Grab a large rock',
            'Try and make a run for it',
            'Attack the wolf unarmed'
        ]
    })
    print 'The wolf mauls you. You die. The end.'

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print 'Aborted.'
