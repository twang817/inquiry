from prompt_toolkit.layout.containers import Window
from prompt_toolkit.mouse_events import MouseEventTypes


def find_in_layout(cli, name):
    for child in cli.layout.walk(cli):
        if isinstance(child, Window) and getattr(child.content, 'name', None) == name:
            yield child.content

def if_mousedown(handler):
    def handle_if_mouse_down(cli, mouse_event):
        if mouse_event.event_type == MouseEventTypes.MOUSE_DOWN:
            return handler(cli, mouse_event)
        return NotImplemented

    return handle_if_mouse_down
