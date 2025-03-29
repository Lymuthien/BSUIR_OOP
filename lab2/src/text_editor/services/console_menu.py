import os
import time

from .editor import Editor
from ..interfaces import IFileManager


class ConsoleMenu(object):
    def __init__(self, savers: dict[str, IFileManager], editor: Editor):
        self._savers = savers
        self._editor = editor

    def save_menu(self) -> None:
        menu = ['Docs: md, txt, rtf',
                'Formats: json, xml',
                'Savers: [local], [cloud]',
                'Enter filepath, doc, and format through space (ex. docs\my_doc md json local): ']

        os.system('cls')
        for item in menu:
            print(item)

        try:
            cmd = input().strip().lower().split()
            if len(cmd) != 4:
                raise ValueError('Invalid input.')

            if cmd[3] not in self._savers:
                raise ValueError('Unknown saver.')

            self._editor.set_file_manager(self._savers[cmd[3]])
            self._editor.save_document(filepath=cmd[0], extension=cmd[1], format_=cmd[2])
            return
        except Exception as e:
            print(e)
            time.sleep(1.5)

    def set_role_menu(self) -> None:
        os.system('cls')
        name = input('Enter name: ')
        role = input('Enter role (EditorUser, Admin, ReaderUser): ')
        try:
            os.system('cls')
            self._editor.give_role(name, role)
        except Exception as e:
            print(e)
            time.sleep(1.5)

    def login_menu(self) -> None:
        os.system('cls')
        name = input('Enter name: ').strip()
        try:
            self._editor.login(name)
        except Exception as e:
            print(e)
            time.sleep(1.5)

    def open_menu(self):
        os.system('cls')
        cmd = input('Enter space ([local], [cloud]): ').strip().lower()

        try:
            self._editor.set_file_manager(self._savers[cmd])
            self._editor.open_document(input('Enter filepath (ex. data\doc.txt): '))
        except Exception as e:
            print(e)
            time.sleep(1.5)

    def register_menu(self):
        os.system('cls')
        name = input('Enter name: ').strip()

        try:
            self._editor.register(name)
        except Exception as e:
            print(e)
            time.sleep(1.5)

    def main_menu(self, method: callable, height, width) -> None:
        error_msg = ''
        main_menu = ['[R]egister',
                     '[L]ogin',
                     '[Lo]gut',
                     '[C]reate document',
                     '[O]pen document',
                     '[D]elete document',
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
                    case 'r':
                        os.system('cls')
                        self.register_menu()
                    case 'l':
                        os.system('cls')
                        self.login_menu()
                    case 'lo':
                        self._editor.logout()
                    case 'c':
                        os.system('cls')
                        self._editor.create_document()
                        while self._editor.is_opened():
                            method()
                    case 'o':
                        self.open_menu()
                        while self._editor.is_opened():
                            method()

                    case 'd':
                        self.delete_menu()

                    case 'e':
                        os.system('cls')
                        exit()

                    case _:
                        error_msg = 'Invalid input.'

            except Exception as e:
                error_msg = str(e)

    def delete_menu(self) -> None:
        os.system('cls')
        cmd = input('Enter space ([local], [cloud]): ').strip().lower()

        try:
            self._editor.set_file_manager(self._savers[cmd])
            self._editor.delete_document(input('Enter filepath (ex. data\doc.txt): '))
        except Exception as e:
            print(e)
            time.sleep(1.5)
