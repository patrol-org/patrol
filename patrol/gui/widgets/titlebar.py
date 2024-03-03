# This file is part of patrol, fork of range.
# License: GNU GPL version 3, see the file "AUTHORS" for details.

"""The titlebar is the widget at the top, giving you broad overview.

It displays the current path among other things.
"""

from __future__ import (absolute_import, division, print_function)

from os.path import basename

from ranger.gui.bar import Bar

from . import Widget


class TitleBar(Widget):
    old_thisfile = None
    old_keybuffer = None
    old_wid = None
    result = None
    right_sumsize = 0
    throbber = ' '
    need_redraw = False

    def __init__(self, *args, **keywords):
        Widget.__init__(self, *args, **keywords)
        self.cli.signal_bind('tab.change', self.request_redraw, weak=True)

    def request_redraw(self):
        self.need_redraw = True

    def draw(self):
        if self.need_redraw or \
                self.cli.thisfile != self.old_thisfile or\
                str(self.cli.ui.keybuffer) != str(self.old_keybuffer) or\
                self.wid != self.old_wid:
            self.need_redraw = False
            self.old_wid = self.wid
            self.old_thisfile = self.cli.thisfile
            self._calc_bar()
        self._print_result(self.result)
        if self.wid > 2:
            self.color('in_titlebar', 'throbber')
            self.addnstr(self.y, self.wid - self.right_sumsize, self.throbber, 1)

    def click(self, event):
        """Handle a MouseEvent"""
        direction = event.mouse_wheel_direction()
        if direction:
            self.cli.tab_move(direction)
            self.need_redraw = True
            return True

        if not event.pressed(1) or not self.result:
            return False

        pos = self.wid - 1
        for tabname in reversed(self.cli.get_tab_list()):
            tabtext = self._get_tab_text(tabname)
            pos -= len(tabtext)
            if event.x > pos:
                self.cli.tab_open(tabname)
                self.need_redraw = True
                return True

        pos = 0
        for i, part in enumerate(self.result):
            pos += len(part)
            if event.x < pos:
                if self.settings.hostname_in_titlebar and i <= 2:
                    self.cli.enter_dir("~")
                else:
                    if 'directory' in part.__dict__:
                        self.cli.enter_dir(part.directory)
                return True
        return False

    def _calc_bar(self):
        bar = Bar('in_titlebar')
        self._get_left_part(bar)
        self._get_right_part(bar)
        try:
            bar.shrink_from_the_left(self.wid)
        except ValueError:
            bar.shrink_by_removing(self.wid)
        self.right_sumsize = bar.right.sumsize()
        self.result = bar.combine()

    def _get_left_part(self, bar):
        # TODO: Properly escape non-printable chars without breaking unicode
        if self.settings.hostname_in_titlebar:
            if self.cli.username == 'root':
                clr = 'bad'
            else:
                clr = 'good'

            bar.add(self.cli.username, 'hostname', clr, fixed=True)
            bar.add('@', 'hostname', clr, fixed=True)
            bar.add(self.cli.hostname, 'hostname', clr, fixed=True)
            bar.add(' ', 'hostname', clr, fixed=True)

        if self.cli.thisdir:
            pathway = self.cli.thistab.pathway
            if self.settings.tilde_in_titlebar \
                and (self.cli.thisdir.path.startswith(
                    self.cli.home_path + "/") or self.cli.thisdir.path == self.cli.home_path):
                pathway = pathway[self.cli.home_path.count('/') + 1:]
                bar.add('~/', 'directory', fixed=True)

            for path in pathway:
                if path.is_link:
                    clr = 'link'
                else:
                    clr = 'directory'

                bidi_basename = self.bidi_transpose(path.basename)
                bar.add(bidi_basename, clr, directory=path)
                bar.add('/', clr, fixed=True, directory=path)

            if self.cli.thisfile is not None and \
                    self.settings.show_selection_in_titlebar:
                bidi_file_path = self.bidi_transpose(self.cli.thisfile.relative_path)
                bar.add(bidi_file_path, 'file')
        else:
            path = self.cli.thistab.path
            if self.settings.tilde_in_titlebar \
                and (self.cli.thistab.path.startswith(
                    self.cli.home_path + "/") or self.cli.thistab.path == self.cli.home_path):
                path = path[len(self.cli.home_path + "/"):]
                bar.add('~/', 'directory', fixed=True)

            clr = 'directory'
            bar.add(path, clr, directory=path)
            bar.add('/', clr, fixed=True, directory=path)

    def _get_right_part(self, bar):
        # TODO: fix that pressed keys are cut off when chaining CTRL keys
        kbuf = str(self.cli.ui.keybuffer)
        self.old_keybuffer = kbuf
        bar.addright(' ', 'space', fixed=True)
        bar.addright(kbuf, 'keybuffer', fixed=True)
        bar.addright(' ', 'space', fixed=True)
        if len(self.cli.tabs) > 1:
            for tabname in self.cli.get_tab_list():
                tabtext = self._get_tab_text(tabname)
                clr = 'good' if tabname == self.cli.current_tab else 'bad'
                bar.addright(tabtext, 'tab', clr, fixed=True)

    def _get_tab_text(self, tabname):
        result = ' ' + str(tabname)
        if self.settings.dirname_in_tabs:
            dirname = basename(self.cli.tabs[tabname].path)
            if not dirname:
                result += ":/"
            elif len(dirname) > 15:
                result += ":" + dirname[:14] + self.ellipsis[self.settings.unicode_ellipsis]
            else:
                result += ":" + dirname
        return result

    def _print_result(self, result):
        self.win.move(0, 0)
        for part in result:
            self.color(*part.lst)
            y, x = self.win.getyx()
            self.addstr(y, x, str(part))
        self.color_reset()
