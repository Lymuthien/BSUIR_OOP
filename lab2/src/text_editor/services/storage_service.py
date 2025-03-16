from typing import AnyStr

from ..interfaces.istorage_strategy import IStorageStrategy


class LocalStorage(IStorageStrategy):
    def save(self, data, location: str) -> None:
        with open(location, "w") as file:
            file.write(data)

    def load(self, location: str) -> AnyStr:
        with open(location, "r") as file:
            return file.read()
