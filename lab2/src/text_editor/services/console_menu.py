import os
import time

from .editor import Editor
from ..interfaces import IFileManager


class ConsoleMenu(object):
    def __init__(self, savers: dict[str, IFileManager]):
        self._savers = savers

    def save_menu(self, editor: Editor) -> None:
        error_msg = ''
        menu = ['Docs: md, txt, rtf'
                'Formats: txt, json, xml',
                'Savers: [local], [cloud]',
                'Enter filepath, doc, and format through space (ex. docs\my_doc md txt local): ']

        while True:
            os.system('cls')
            print(error_msg)
            for item in menu:
                print(item)

            try:
                cmd = input().strip().lower().split()
                if len(cmd) != 4:
                    raise ValueError('Invalid input.')

                editor.set_file_manager(self._savers[cmd[3]])
                editor.save_document(filepath=cmd[0], extension=cmd[1], format_=cmd[2])
                return
            except Exception as e:
                raise

    @staticmethod
    def login_menu(editor: Editor) -> None:
        os.system('cls')
        password = input('Enter doc password: ').strip()
        try:
            editor.login_as_admin(password)
        except Exception as e:
            print(e)
            time.sleep(1.5)

    def open_menu(self, editor: Editor):
        os.system('cls')
        cmd = input('Enter space ([local], [cloud]): ').strip().lower()

        try:
            editor.set_file_manager(self._savers[cmd])
            editor.open_document(input('Enter filepath (ex. data\doc.txt): '))
        except Exception as e:
            print(e)
            time.sleep(1.5)

    def main_menu(self, editor: Editor, method: callable, height, width) -> None:
        error_msg = ''
        main_menu = ['[C]reate - create new document',
                     '[O]pen - open document',
                     '[D]elete - delete document',
                     '[E]xit']

        while True:
            os.system('cls')
            print(error_msg.center(width))
            print('\n' * (int(height / 2) - len(main_menu)))
            for string in main_menu:
                print(string.center(width))

            error_msg = ''
            cmd = input().strip().lower()
            try:
                match cmd:
                    case 'c':
                        os.system('cls')
                        print(editor.create_document())
                        input('\nRemember this password. Press Enter to continue.')
                        while editor.is_opened():
                            method()
                    case 'o':
                        self.open_menu(editor)
                        while editor.is_opened():
                            method()

                    case 'd':
                        self.delete_menu(editor)

                    case 'e':
                        os.system('cls')
                        exit()

                    case _:
                        error_msg = 'Invalid input.'

            except Exception as e:
                error_msg = str(e)

    def delete_menu(self, editor: Editor) -> None:
        os.system('cls')
        cmd = input('Enter space ([local], [cloud]): ').strip().lower()

        try:
            editor.set_file_manager(self._savers[cmd])
            editor.delete_document(input('Enter filepath (ex. data\doc.txt): '))
        except Exception as e:
            print(e)
            time.sleep(1.5)
