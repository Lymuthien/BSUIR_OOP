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

from text_editor.editor import Editor


class ConsoleEditor(object):
    def __init__(self):
        self.__editor = Editor()
        self._width = os.get_terminal_size().columns
        self._height = os.get_terminal_size().lines

        self._styles = Style.from_dict({
            'default': 'white',
        })

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

    def _save_menu(self) -> None:
        error_msg = ''
        menu = ['Docs: md, txt, rtf'
                'Formats: txt, json, xml',
                'Savers: [l]ocal, [d]atabase',
                'Enter filepath, doc, and format through space (ex. docs\my_doc md txt l): ']

        while True:
            os.system('cls')
            print(error_msg)
            for item in menu:
                print(item)

            try:
                cmd = input().strip().lower().split()
                if len(cmd) != 4:
                    raise ValueError('Invalid input.')

                if cmd[3] == 'l':
                    flag = True
                elif cmd[3] == 'd':
                    flag = False
                else:
                    raise ValueError('Invalid input.')

                self.__editor.save_document(cmd[0], cmd[1], cmd[2], local=flag)
                return
            except Exception as e:
                error_msg = str(e)

    def _login_menu(self) -> None:
        os.system('cls')
        password = input('Enter doc password: ').strip()
        try:
            self.__editor.login_as_admin(password)
        except Exception as e:
            print(e)
            time.sleep(3)

    def _set_key_bindings(self, kb: KeyBindings):
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
                self.__editor.apply_bold(select_indexes[0], select_indexes[1])
                event.current_buffer.text = self.__editor.get_text()

        @kb.add('c-i')
        def apply_italic(event):
            select_indexes = self._select_text(event.current_buffer)
            if select_indexes:
                self.__editor.apply_italic(select_indexes[0], select_indexes[1])
                event.current_buffer.text = self.__editor.get_text()

        @kb.add('c-c')
        def copy(event):
            select_indexes = self._select_text(event.current_buffer)
            if select_indexes:
                pyperclip.copy(event.current_buffer.text[select_indexes[0]:select_indexes[1] + 1])

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
            self._save_menu()
            time.sleep(1)

        @kb.add('c-l')
        def login(event):
            event.app.exit()
            self._login_menu()

        @kb.add('c-r')
        def read_only(event):
            self.__editor.set_read_only(not self.__editor.read_only())
            event.app.exit()
            self.__editor.close_document()

    def _open_menu(self):
        os.system('cls')
        error_msg = ''
        while True:
            print(error_msg)
            cmd = input('Enter space ([L]ocal or [D]atabase): ').strip().lower()

            try:
                if cmd == 'l':
                    flag = True
                elif cmd == 'd':
                    flag = False
                else:
                    raise ValueError('Invalid input.')

                self.__editor.open_document(input('Enter filename: '), flag)
                return
            except Exception as e:
                error_msg = str(e)


    def run_main_menu(self):
        error_msg = ''
        main_menu = ['[C]reate - create new document',
                     '[O]pen - open document',
                     '[D]elete - delete document',
                     '[E]xit']

        while True:
            os.system('cls')
            print(error_msg)
            print('\n' * (int(self._height / 2) - len(main_menu)))
            for string in main_menu:
                print(string.center(self._width))

            error_msg = ''
            cmd = input().strip().lower()
            try:
                match cmd:
                    case 'c':
                        os.system('cls')
                        print(self.__editor.create_document())
                        input('\nRemember this password. Press Enter to continue.')

                        while self.__editor.is_opened():
                            self.run_editor_space()

                    case 'o':
                        self._open_menu()
                        while self.__editor.is_opened():
                            self.run_editor_space()

                    case 'd':
                        os.system('cls')
                        cmd = input('Enter path to document: ')
                        pass

                    case 'e':
                        os.system('cls')
                        exit()
                    case _:
                        raise Exception('Invalid command')

            except Exception as e:
                error_msg = str(e)

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

    def run_editor_space(self):
        basic_text = self.__editor.get_text()

        buffer = Buffer(read_only=self.__editor.read_only(),
                        on_text_changed=lambda buff: self._on_text_changed(buff.text, buffer.cursor_position))
        buffer.text = basic_text

        window = Window(content=BufferControl(buffer=buffer), style='class:default')
        app = Application(layout=Layout(window), key_bindings=self.__kb, full_screen=True, style=self._styles)

        app.run()


if __name__ == '__main__':
    console = ConsoleEditor()
    console.run_main_menu()
