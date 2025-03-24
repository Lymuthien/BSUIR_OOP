import os
import time

from .editor import Editor


class ConsoleMenu(object):
    @staticmethod
    def save_menu(editor: Editor) -> None:
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

                if cmd[3] != 'l' and cmd[3] != 'd':
                    raise ValueError('Invalid input.')
                flag = True if cmd[3] == 'l' else False

                editor.save_document(cmd[0], cmd[1], cmd[2], local=flag)
                return
            except Exception as e:
                error_msg = str(e)

    @staticmethod
    def login_menu(editor: Editor) -> None:
        os.system('cls')
        password = input('Enter doc password: ').strip()
        try:
            editor.login_as_admin(password)
        except Exception as e:
            print(e)
            time.sleep(1.5)

    @staticmethod
    def open_menu(editor: Editor):
        os.system('cls')
        cmd = input('Enter space ([L]ocal or [D]atabase): ').strip().lower()

        try:
            if cmd != 'l' and cmd != 'd':
                raise ValueError('Invalid input.')
            flag = True if cmd == 'l' else False

            editor.open_document(input('Enter filepath (ex. data\doc.txt): '), flag)
        except Exception as e:
            print(e)
            time.sleep(1.5)

    @staticmethod
    def main_menu(editor: Editor, method: callable, height, width) -> None:
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
                        ConsoleMenu.open_menu(editor)
                        while editor.is_opened():
                            method()

                    case 'd':
                        ConsoleMenu.delete_menu(editor)

                    case 'e':
                        os.system('cls')
                        exit()

                    case _:
                        error_msg = 'Invalid input.'

            except Exception as e:
                error_msg = str(e)

    @staticmethod
    def delete_menu(editor: Editor) -> None:
        os.system('cls')
        cmd = input('Enter space ([L]ocal or [D]atabase): ').strip().lower()

        try:
            if cmd != 'l' and cmd != 'd':
                raise ValueError('Invalid input.')
            flag = True if cmd == 'l' else False

            editor.delete_document(input('Enter filepath (ex. data\doc.txt): '), flag)
        except Exception as e:
            print(e)
            time.sleep(1.5)
