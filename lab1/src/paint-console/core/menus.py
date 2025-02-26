from ..interfaces import IAddableMenu, IMenuItem


class MainMenu(IAddableMenu):
    def __init__(self):
        self.__items = {}

    def add_item(self, key: str, item: IMenuItem):
        self.__items[key] = item

    def execute(self):
        while True:
            print("0 - Exit (without saving)"
                  "1 - Choose figure"
                  "2 - Object selection"
                  "3 - Save file"
                  "4 - Load file"
                  "5 - Undo"
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
            print("1 - Rectangle"
                  "2 - Triangle"
                  "3 - Ellipse"
                  "0 - Exit")
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
            print("i - Info")
            print("← → - Navigate")
            print("m - Move")
            print("e - Erase")
            print("bg - Change background")
            print("0 - Exit")
            choice = input("Select action: ").lower()

            if choice == '0':
                break
            self.__items.get(choice, lambda: print("Invalid action!")).execute()
