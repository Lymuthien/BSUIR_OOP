import secrets

from ..models import ChangeStyleCommand, WriteCommand, EraseCommand, ChangeThemeCommand, Admin, EditorUser, ReaderUser, \
    User, MarkdownDocument, MdToRichTextAdapter, MdToPlainTextAdapter, Theme, DocumentToJsonSerializerAdapter, \
    DocumentToXmlSerializerAdapter, DocumentToTxtSerializerAdapter
from .history_manager import HistoryManager
from .file_manager import DatabaseFileManager, LocalFileManager


class Editor(object):
    def __init__(self):
        self.__history: HistoryManager = HistoryManager()

        self.__serializers: dict = {'txt': DocumentToTxtSerializerAdapter(MarkdownDocument()),
                                    'xml': DocumentToXmlSerializerAdapter(MarkdownDocument()),
                                    'json': DocumentToJsonSerializerAdapter(MarkdownDocument()), }
        self.__themes: list[Theme] = [Theme(1, True, True), Theme(2, False, True),
                                      Theme(3, True, True), Theme(4, False, True),
                                      Theme(5, True, True),]
        self.__current_password: str | None = None
        self.__doc: MarkdownDocument | None = None
        self.__current_user: User | None = None

    def create_document(self) -> str:
        self.__current_user = Admin()
        self.__doc = MarkdownDocument()
        self.__doc.attach(self.__current_user)
        password = secrets.token_urlsafe(8)
        self.__doc.set_password(password)

        return password

    def open_document(self,
                      filename: str,
                      local: bool = True):
        loader = LocalFileManager if local else DatabaseFileManager
        extension = filename.split('.')[-1].lower()

        try:
            serializer = self.__serializers[extension]
        except KeyError:
            raise Exception('Unknown format')

        doc = loader.load(filename, serializer)
        if self.__doc:
            self.__doc.detach(self.__current_user)

        self.__doc = doc
        self.__current_user = ReaderUser() if self.__doc.settings.read_only else EditorUser()
        self.__doc.attach(self.__current_user)

    def close_document(self):
        self.__doc.detach(self.__current_user)
        self.__doc = None
        self.__current_user = None
        self.__history.clear()

    def save_document(self,
                      filepath: str,
                      extension: str = 'md',
                      format_: str = 'txt',
                      local: bool = True):
        saver = LocalFileManager if local else DatabaseFileManager
        extension = extension.lower().strip()
        format_ = format_.lower().strip()

        try:
            serializer = self.__serializers[format_]
        except KeyError:
            raise Exception('Unknown format')

        file_extension = None if format != 'txt' else extension

        if extension == 'md':
            saver.save(self.__doc, filepath, serializer, extension=file_extension)
        elif extension == 'rtf':
            saver.save(MdToRichTextAdapter(self.__doc), filepath, serializer, extension=file_extension)
        elif extension == 'txt':
            saver.save(MdToPlainTextAdapter(self.__doc), filepath, serializer, extension=file_extension)
        else:
            raise Exception('Unknown extension')

    def login_as_admin(self,
                       password: str):
        if self.__doc.validate_password(password):
            self.__doc.detach(self.__current_user)
            self.__current_user = Admin()
            self.__doc.attach(self.__current_user)
        else:
            raise Exception('Invalid password')

    def undo(self):
        self.__history.undo()

    def redo(self):
        self.__history.redo()

    def insert_text(self,
                    text: str,
                    position: int):
        if not self.__current_user.can_edit_text():
            raise Exception('User cant edit text')

        command = WriteCommand(text, position, self.__doc)
        command.execute()
        self.__history.add_command(command)

    def erase_text(self,
                   start: int,
                   end: int):
        if not self.__current_user.can_edit_text():
            raise Exception('User cant edit text')

        command = EraseCommand(start, end, self.__doc)
        command.execute()
        self.__history.add_command(command)

    def apply_bold(self,
                   start: int,
                   end: int):
        if not self.__current_user.can_edit_text():
            raise Exception('User cant edit text')

        command = ChangeStyleCommand(start, end, self.__doc, bold=True)
        command.execute()
        self.__history.add_command(command)

    def apply_italic(self,
                     start: int,
                     end: int):
        if not self.__current_user.can_edit_text():
            raise Exception('User cant edit text')

        command = ChangeStyleCommand(start, end, self.__doc, italic=True)
        command.execute()
        self.__history.add_command(command)

    def set_theme(self,
                  theme_number: int):
        if not self.__current_user.can_edit_text():
            raise Exception('User cant edit text')

        command = ChangeThemeCommand(self.__doc, self.__themes[theme_number - 1])
        command.execute()
        self.__history.add_command(command)

    def read_only(self) -> bool:
        return self.__doc.settings.read_only

    def set_read_only(self,
                      read_only: bool):
        if not self.__current_user.can_change_document_settings():
            raise Exception('User cant change document settings')

        self.__doc.settings.read_only = read_only

    def get_text(self):
        return self.__doc.get_text()

    def is_opened(self) -> bool:
        return self.__doc is not None
