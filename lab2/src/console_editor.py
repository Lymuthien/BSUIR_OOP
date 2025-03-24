import os
import time

import pyperclip
from prompt_toolkit import Application
from prompt_toolkit.buffer import Buffer
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout.containers import Window
from prompt_toolkit.layout.controls import BufferControl
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.styles import Style

from text_editor.services import Editor, ConsoleMenu


class ConsoleEditor(object):
    def __init__(self):
        self.__editor = Editor()
        self._width = os.get_terminal_size().columns
        self._height = os.get_terminal_size().lines

        font_sizes = map(str, self.__editor.settings.font_sizes)
        colors = ('red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white')
        self.__styles = Style([*zip(font_sizes, colors)])
        self.__kb = KeyBindings()
        self._set_key_bindings(self.__kb)

    @staticmethod
    def _select_text(buffer: Buffer) -> tuple | None:
        if buffer.selection_state is not None:
            start_position = buffer.selection_state.original_cursor_position
            end_position = buffer.cursor_position

            if end_position < start_position:
                start_position, end_position = end_position, start_position

            end_position -= 1
            return start_position, end_position

    def _set_key_bindings(self, kb: KeyBindings):
        @kb.add('c-t')
        def increase_font(event):
            self.__editor.settings.font_size = self.__editor.settings.font_size + 1
            event.app.layout.container.style = f'class:{self.__editor.settings.font_size}'

        @kb.add('c-u')
        def decrease_font(event):
            self.__editor.settings.font_size = self.__editor.settings.font_size - 1
            event.app.layout.container.style = f'class:{self.__editor.settings.font_size}'

        @kb.add('c-d')
        def exit_app(event):
            event.app.exit()
            self.__editor.close_document()

        @kb.add('c-z')
        def undo(event):
            self.__editor.undo()
            event.current_buffer.text = self.__editor.get_text()

        @kb.add('c-y')
        def redo(event):
            self.__editor.redo()
            event.current_buffer.text = self.__editor.get_text()

        @kb.add('c-b')
        def apply_bold(event):
            select_indexes = self._select_text(event.current_buffer)
            if select_indexes:
                self.__editor.apply_style(select_indexes[0], select_indexes[1], bold=True)
                event.current_buffer.text = self.__editor.get_text()

        @kb.add('c-i')
        def apply_italic(event):
            select_indexes = self._select_text(event.current_buffer)
            if select_indexes:
                self.__editor.apply_style(select_indexes[0], select_indexes[1], italic=True)
                event.current_buffer.text = self.__editor.get_text()

        @kb.add('c-c')
        def copy(event):
            select_indexes = self._select_text(event.current_buffer)
            if select_indexes:
                pyperclip.copy(event.current_buffer.text[select_indexes[0]:select_indexes[1] + 1])

        @kb.add('c-n')
        def apply_strikethrough(event):
            select_indexes = self._select_text(event.current_buffer)
            if select_indexes:
                self.__editor.apply_style(select_indexes[0], select_indexes[1], strikethrough=True)
                event.current_buffer.text = self.__editor.get_text()

        @kb.add('c-v')
        def paste(event):
            text = pyperclip.paste()
            self.__editor.insert_text(text, event.current_buffer.cursor_position)
            event.current_buffer.text = self.__editor.get_text()

        def set_theme_handler(theme_number: int) -> callable:
            def handler(event):
                self.__editor.set_theme(theme_number)
                event.current_buffer.text = self.__editor.get_text()

            return handler

        for i in range(1, 6):
            kb.add(f'f{i}')(set_theme_handler(i))

        @kb.add('c-s')
        def save(event):
            event.app.exit()
            ConsoleMenu.save_menu(self.__editor)
            time.sleep(1)

        @kb.add('c-l')
        def login(event):
            event.app.exit()
            ConsoleMenu.login_menu(self.__editor)

        @kb.add('c-r')
        def read_only(event):
            self.__editor.set_read_only(not self.__editor.read_only())
            event.app.exit()
            ConsoleMenu.save_menu(self.__editor)
            self.__editor.close_document()

    def _on_text_changed(self, new_text: str, cursor_position: int):
        old_text = self.__editor.get_text()

        old_len = len(old_text)
        new_len = len(new_text)
        if new_len > old_len:
            cursor_position -= 1
            self.__editor.insert_text(new_text[cursor_position:cursor_position + new_len - old_len], cursor_position)
        elif old_len == new_len:
            return
        else:
            self.__editor.erase_text(cursor_position, cursor_position + old_len - new_len - 1)

    def _run_editor_space(self):
        buffer = Buffer(on_text_changed=lambda buff: self._on_text_changed(buff.text, buffer.cursor_position))
        buffer.text = self.__editor.get_text()
        buffer.read_only = self.__editor.read_only

        window = Window(content=BufferControl(buffer=buffer), style=f'class:{self.__editor.settings.font_size}')
        app = Application(layout=Layout(window), key_bindings=self.__kb, full_screen=True, style=self.__styles)

        app.run()

    def run(self):
        ConsoleMenu.main_menu(self.__editor, self._run_editor_space, self._height, self._width)


if __name__ == '__main__':
    console = ConsoleEditor()
    console.run()
