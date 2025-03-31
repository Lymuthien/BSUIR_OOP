from typing import final

from .theme import Theme
from ..interfaces import ICommand, IDocument


@final
class WriteCommand(ICommand):
    def __init__(self,
                 text: str,
                 pos: int,
                 doc: IDocument) -> None:
        self.__text = text
        self.__pos = pos
        self.__doc = doc

    def execute(self) -> None:
        self.__doc.insert_text(self.__text, self.__pos)

    def undo(self) -> None:
        self.__doc.delete_text(self.__pos, self.__pos + len(self.__text) - 1)

    def redo(self) -> None:
        self.execute()


@final
class EraseCommand(ICommand):
    def __init__(self,
                 start: int,
                 end: int,
                 doc: IDocument) -> None:
        self.__start = start
        self.__end = end
        self.__doc = doc
        self.__deleted_text = self.__doc.get_text()[self.__start:self.__end + 1]

    def execute(self) -> None:
        self.__doc.delete_text(self.__start, self.__end)

    def undo(self) -> None:
        self.__doc.insert_text(self.__deleted_text, self.__start)

    def redo(self) -> None:
        self.execute()


@final
class ChangeStyleCommand(ICommand):
    def __init__(self,
                 start: int,
                 end: int,
                 doc: IDocument,
                 bold: bool = False,
                 italic: bool = False,
                 strikethrough: bool = False) -> None:
        self.__start = start
        self.__end = end
        self.__doc = doc
        self.__bold = bold
        self.__italic = italic
        self.__strikethrough = strikethrough
        self.__old_text = doc.get_text()
        self.__new_text = None

    def execute(self) -> None:
        from .documents.md_document import MarkdownDocument
        assert isinstance(self.__doc, MarkdownDocument), "Invalid document instance"

        if self.__bold:
            self.__doc.apply_bold(self.__start, self.__end)
        if self.__italic:
            self.__doc.apply_italic(self.__start, self.__end)
        if self.__strikethrough:
            self.__doc.apply_strikethrough(self.__start, self.__end)
        self.__new_text = self.__doc.get_text()

    def undo(self) -> None:
        self.__doc.replace_text(self.__old_text, 0, len(self.__new_text) - 1)

    def redo(self) -> None:
        self.__doc.replace_text(self.__new_text, 0, len(self.__old_text) - 1)


@final
class ChangeThemeCommand(ICommand):
    def __init__(self,
                 doc: IDocument,
                 theme: Theme) -> None:
        self.__doc = doc
        self.__theme = theme
        self.__old_text = doc.get_text()
        self.__new_text = None

    def execute(self) -> None:
        self.__doc.set_theme(self.__theme)
        self.__new_text = self.__doc.get_text()

    def undo(self) -> None:
        self.__doc.replace_text(self.__old_text, 0, len(self.__new_text) - 1)

    def redo(self) -> None:
        self.__doc.replace_text(self.__new_text, 0, len(self.__old_text) - 1)
