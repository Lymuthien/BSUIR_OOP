from ..interfaces import IAddableMenu, IMenuItem


class MainMenu(IAddableMenu):
    def __init__(self):
        self.__items = {}

    def add_item(self, key: str, item: IMenuItem):
        self.__items[key] = item

    def execute(self):
        while True:
            print("0 - Exit (without saving)\n"
                  "1 - Choose figure\n"
                  "2 - Object selection\n"
                  "3 - Save file\n"
                  "4 - Load file\n"
                  "5 - Undo\n"
                  "6 - Redo")
            choice = input("Select option: ")

            if choice == '0':
                break
            if choice not in self.__items.keys():
                print("Invalid option")
                continue
            else:
                self.__items.get(choice).execute()


class FigureMenu(IAddableMenu):
    def __init__(self):
        self.__items = {}

    def add_item(self, key: str, item: IMenuItem):
        self.__items[key] = item

    def execute(self):
        while True:
            print("0 - Exit to menu\n"
                  "1 - Rectangle\n"
                  "2 - Triangle\n"
                  "3 - Ellipse\n")
            choice = input("Select figure: ")

            if choice == '0':
                break
            if choice not in self.__items.keys():
                print("Invalid option")
                continue
            else:
                self.__items.get(choice).execute()


class ObjectMenu(IAddableMenu):
    def __init__(self):
        self.__items = {}

    def add_item(self, key: str, item: IMenuItem):
        self.__items[key] = item

    def execute(self):
        while True:
            print("0 - Exit to menu\n"
                  "i - Info\n"
                  "n - Next figure\n"
                  "p - Previous figure\n"
                  "m - Move\n"
                  "e - Erase\n"
                  "bg - Change background\n")
            choice = input("Select action: ").lower()

            if choice == '0':
                break
            if choice not in self.__items.keys():
                print("Invalid option")
                continue
            else:
                self.__items.get(choice).execute()
