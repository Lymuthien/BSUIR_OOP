from typing import Any

from ..interfaces import INavigator


class Navigator(INavigator):
    def __init__(self, *args):
        """
        Create list of objects, that can be navigated.
        :param args: default values for navigation
        """
        self.__objects = [*args]
        self.__current_index = len(args) - 1 if args else None

    def append(self, item) -> None:
        """Append item to navigation list."""
        self.__objects.append(item)
        self.__current_index = self.__objects.index(item)

    def remove(self, item) -> None:
        """Remove item from navigation list if it exists."""
        if item in self.__objects:
            self.__objects.remove(item)
            if self.__current_index >= len(self.__objects) > 0:
                self.prev()
            elif len(self.__objects) <= 0:
                self.__current_index = None
        else:
            raise IndexError("No such object")

    def next(self) -> Any:
        """Return next item in navigation list if it is not empty."""
        if not self.__current_index is None:
            self.__current_index = (self.__current_index + 1) % len(self.__objects)
            return self.__objects[self.__current_index]
        else:
            raise IndexError("List empty")

    def prev(self) -> Any:
        """Return previous item in navigation list if it is not empty."""
        if not self.__current_index is None:
            self.__current_index = (self.__current_index - 1) % len(self.__objects)
            return self.__objects[self.__current_index]
        else:
            raise IndexError("List empty")

    def current(self):
        """Return current item in navigation list if it is not empty."""
        if not self.__current_index is None:
            return self.__objects[self.__current_index]
        else:
            raise IndexError("List empty")
