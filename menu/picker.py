import curses
import os
import platform

KEYS_ENTER = (curses.KEY_ENTER, ord('\n'), ord('\r'))
KEYS_UP = (curses.KEY_UP, ord('k'))
KEYS_DOWN = (curses.KEY_DOWN, ord('j'))
KEYS_SELECT = (curses.KEY_RIGHT, ord(' '))
KEYS_QWERTY = 'qwertyuiopasdfghjklzxcvbnm'


class Picker(object):
    def __init__(self, options: list, title=None, indicator='*', default_index=0, multi_select=False,
                 min_selection_count=0,
                 options_map_func=None, should_filter_options=False, select_all=False, map_options=True):

        if len(options) == 0:
            raise ValueError('options should not be an empty list')

        self.options = self.filter_options(options) if should_filter_options else options
        self.title = title
        self.indicator = indicator
        self.multi_select = multi_select
        self.min_selection_count = min_selection_count
        self.options_map_func = options_map_func
        self.should_filter_options = should_filter_options
        self.all_selected = []
        if select_all:
            for index, option in enumerate(self.options):
                self.all_selected.append(index)
        if default_index >= len(options):
            raise ValueError('default_index should be less than the length of options')

        if multi_select and min_selection_count > len(options):
            raise ValueError(
                'min_selection_count is bigger than the available options, you will not be able to make any selection')

        if options_map_func is not None and not callable(options_map_func):
            raise ValueError('options_map_func must be a callable function')

        self.index = default_index
        self.custom_handlers = {}
        self._map_options = map_options
        self.custom_handler_options_map = self.map_option_handlers(self.options)

    def register_custom_handler(self, key, func):
        self.custom_handlers[key] = func

    def move_up(self):
        self.index -= 1
        if self.index < 0:
            self.index = len(self.options) - 1

    def move_down(self):
        self.index += 1
        if self.index >= len(self.options):
            self.index = 0

    def mark_index(self):
        if self.multi_select:
            if self.index in self.all_selected:
                self.all_selected.remove(self.index)
            else:
                self.all_selected.append(self.index)

    def get_selected(self):
        """return the current selected option as a tuple: (option, index)
           or as a list of tuples (in case multi_select==True)
        """
        if self.multi_select:
            return_tuples = []
            for selected in self.all_selected:
                return_tuples.append((self.options[selected], selected))
            return return_tuples
        else:
            return self.options[self.index], self.index

    def get_title_lines(self):
        if self.title:
            return self.title.split('\n') + ['']
        return []

    def get_option_lines(self):
        lines = []
        for index, option in enumerate(self.options):
            if self.options_map_func:
                option = self.options_map_func(option)

            if index == self.index:
                prefix = self.indicator
            else:
                prefix = len(self.indicator) * ' '

            if len(self.options) > 35 or self._map_options is False:
                if self.multi_select and index in self.all_selected:
                    format = curses.color_pair(1)
                    line = ('{0} {1}'.format(prefix, option), format)
                else:
                    line = '{0} {1}'.format(prefix, option)
                lines.append(line)
            else:
                if option == 'Exit':
                    button = 0
                else:
                    button = index + 1

                if button > 9:
                    button = KEYS_QWERTY[button - 10]

                if self.multi_select and index in self.all_selected:
                    format = curses.color_pair(1)
                    line = ('{0} [{1}] - {2}'.format(prefix, button, option), format)
                else:
                    line = '{0} [{1}] - {2}'.format(prefix, button, option)
                lines.append(line)

        return lines

    def get_lines(self):
        title_lines = self.get_title_lines()
        option_lines = self.get_option_lines()
        lines = title_lines + option_lines
        current_line = self.index + len(title_lines) + 1
        return lines, current_line

    def filter_options(self, options):
        for option in options.copy():
            if len(option) == 3 and (not bool(option[2]) or option[2] == 'false'):
                options.remove(option)

        return options

    def draw(self):
        """draw the curses ui on the screen, handle scroll if needed"""
        self.screen.clear()

        x, y = 1, 1  # start point
        max_y, max_x = self.screen.getmaxyx()
        max_rows = max_y - y  # the max rows we can draw

        lines, current_line = self.get_lines()

        # calculate how many lines we should scroll, relative to the top
        scroll_top = getattr(self, 'scroll_top', 0)
        if current_line <= scroll_top:
            scroll_top = 0
        elif current_line - scroll_top > max_rows:
            scroll_top = current_line - max_rows
        self.scroll_top = scroll_top

        lines_to_draw = lines[scroll_top:scroll_top + max_rows]

        for line in lines_to_draw:
            if type(line) is list:
                self.screen.addnstr(y, x, line[0], max_x - 2, line[1])
            else:
                self.screen.addnstr(y, x, line, max_x - 2)
            y += 1

        self.screen.refresh()

    def run_loop(self):
        while True:
            self.draw()
            c = self.screen.getch()
            if c in KEYS_UP:
                self.move_up()
            elif c in KEYS_DOWN:
                self.move_down()
            elif c in KEYS_ENTER:
                if self.multi_select and len(self.all_selected) < self.min_selection_count:
                    continue
                return self.get_selected()
            elif c in KEYS_SELECT and self.multi_select:
                self.mark_index()
            elif c in self.custom_handler_options_map:
                if not chr(c).isdigit():
                    return self.options[
                        self.custom_handler_options_map.index(c)], self.custom_handler_options_map.index(c)
                else:
                    return self.options[int(chr(c)) - 1], int(chr(c)) - 1
            elif c in self.custom_handlers:
                ret = self.custom_handlers[c](self)
                if ret:
                    return ret

    def config_curses(self):
        # use the default colors of the terminal
        curses.use_default_colors()
        # hide the cursor
        curses.curs_set(0)
        # add some color for multi_select
        # @todo make colors configurable
        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_WHITE)

    def _start(self, screen):
        self.screen = screen
        self.config_curses()
        return self.run_loop()

    def start(self):
        return curses.wrapper(self._start)

    def get_option_label(self, option):
        return option[0]

    def process_picked_option(self, option):
        if option and option[0] and len(option[0]) in [2, 3]:
            if isinstance(option[0][1], str):
                os.system(option[0][1])

            if callable(option[0][1]):
                option[0][1]()

            return option
        else:
            return option

    def map_option_handlers(self, options):
        mapped_keys = []

        if len(options) > 35 or self._map_options is False:
            return mapped_keys

        for index, option in enumerate(options):
            if option[0] == 'Exit':
                mapped_keys.append(ord('0'))
                continue

            if index < 9:
                mapped_keys.append(ord(str(index + 1)))
            else:
                mapped_keys.append(ord(KEYS_QWERTY[index - 9]))

        return mapped_keys


def pick(options, title=None, indicator='*', default_index=0, multi_select=False, min_selection_count=0,
         options_map_func=None, should_filter_options=False, select_all=False, map_options=True):
    """Construct and start a :class:`Picker <Picker>`.

    Usage::

      >>> from pick import pick
      >>> title = 'Please choose an option: '
      >>> options = ['option1', 'option2', 'option3']
      >>> option, index = pick(options, title)
    """
    picker = Picker(options, title, indicator, default_index, multi_select, min_selection_count, options_map_func,
                    should_filter_options, select_all, map_options)

    picker.register_custom_handler(27, go_back)
    if platform.system() == 'Linux':
        picker.register_custom_handler(263, go_back)
    else:
        picker.register_custom_handler(127, go_back)
    option = picker.start()
    return picker.process_picked_option(option)


def go_back(picker):
    return None, -1
