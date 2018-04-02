from prompt_toolkit.layout.containers import (
    ScrollOffsets,
    Window,
)
from prompt_toolkit.layout.controls import UIContent
from prompt_toolkit.layout.screen import Point


class InfiniteContent(UIContent):
    def __init__(self, content):
        line_count = content.line_count - 1
        lines = [content.get_line(lineno) for lineno in range(line_count)] * 3
        super(InfiniteContent, self).__init__(
            get_line=lambda i: lines[i],
            line_count=len(lines),
            cursor_position=Point(
                x=content.cursor_position.x,
                y=content.cursor_position.y + content.line_count),
            default_char=content.default_char)


class InfiniteWindow(Window):
    def __init__(self, *args, **kwargs):
        super(InfiniteWindow, self).__init__(*args, **kwargs)
        self.vertical_scroll = 0
        self.vertical_scroll_2 = 0
        self.infinite = False

    def _copy_body(self, cli, ui_content, new_screen, write_position, move_x,
                   width, vertical_scroll=0, horizontal_scroll=0,
                   has_focus=False, wrap_lines=False, highlight_lines=False,
                   vertical_scroll_2=0, always_hide_cursor=False):
        original_ui_content = ui_content
        if self.infinite:
            vertical_scroll = vertical_scroll + ui_content.line_count - 1
            ui_content = InfiniteContent(ui_content)

        visible_line_to_row_col, rowcol_to_yx = super(InfiniteWindow, self)._copy_body(
            cli, ui_content, new_screen, write_position, move_x,
            width, vertical_scroll, horizontal_scroll,
            has_focus, wrap_lines, highlight_lines,
            vertical_scroll_2, always_hide_cursor)

        if self.infinite:
            patched_rowcol_to_yx = {}
            for (lineno, col), (ypos, xpos) in rowcol_to_yx.items():
                lineno = lineno % (original_ui_content.line_count - 1)
                patched_rowcol_to_yx[lineno, col] = (ypos, xpos)
            rowcol_to_yx = patched_rowcol_to_yx

        return visible_line_to_row_col, rowcol_to_yx

    def _scroll_when_linewrapping(self, ui_content, width, height, cli):
        # annoyingly, ui_content always contains an empty line at the end
        line_count = ui_content.line_count - 1
        heights = [ui_content.get_height_for_line(line, width) for line in range(line_count)]

        # if there are fewer lines than the window height, just render the content at the very top
        self.infinite = False
        if sum(heights) <= height:
            self.vertical_scroll = 0
            self.vertical_scroll_2 = 0
            return

        self.infinite = True

        cursor_pos = ui_content.cursor_position.y

        # calculate the difference between the cursor position and the scroll position (including the vertical_scroll_2
        # offset). this will tell us where the cursor is within the window
        delta = sum(heights[:cursor_pos]) - sum(heights[:self.vertical_scroll]) + self.vertical_scroll_2
        # use the modulo to get the downward distance (note the potential negative in the modulo)
        distance = delta % line_count
        # anything less than the height is considered a down motion
        if distance < height:
            # allow the top margin to increase up to the middle of the height
            top = min(height / 2, max(self.scroll_offsets.top, distance))
            self.scroll_offsets = ScrollOffsets(top=top)

        # now that the top margin is set, we can proceed to calculate our vertical scroll
        if self.scroll_offsets.top == 0:
            # in the special case that we have no top margin, we simply use our cursor position as the vertical scroll
            # (i.e., put the current line at the very top)
            self.vertical_scroll = cursor_pos
            self.vertical_scroll_2 = 0
        else:
            # otherwise, we start adding the heights of the lines above the cursor position until we have met or
            # exceeded the top margin
            used = 0
            for lineno in range(cursor_pos - 1, cursor_pos - 1 - height, -1):
                used += heights[lineno]
                if used >= self.scroll_offsets.top:
                    # the vertical scroll is set to the line that met or exceeded the top margin
                    self.vertical_scroll = lineno
                    # if we exceeded, we need to know how many lines to shift off of the line used as the vertical
                    # scroll position
                    self.vertical_scroll_2 = used - self.scroll_offsets.top
                    break
            else:
                # error if we somehow did not exceed the top margin (this should never happen)
                raise RuntimeError('BUG')

    def _scroll_without_linewrapping(self):
        raise NotImplementedError('_scroll_without_linewrapping')
