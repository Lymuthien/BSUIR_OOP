from .editor_settings import EditorSettings
from .file_manager import DatabaseFileManager, LocalFileManager
from .history_manager import HistoryManager
from ..interfaces import ICommand
from ..models import ChangeStyleCommand, WriteCommand, EraseCommand, ChangeThemeCommand, Admin, EditorUser, ReaderUser, \
    User, MarkdownDocument, MdToRichTextAdapter, MdToPlainTextAdapter, Theme, DocumentToJsonSerializerAdapter, \
    DocumentToXmlSerializerAdapter, DocumentToTxtSerializerAdapter
from ..models.password_manager import PasswordManager


class Editor(object):
    def __init__(self):
        self.__history: HistoryManager = HistoryManager()

        self.__serializers: dict = {'txt': DocumentToTxtSerializerAdapter(MarkdownDocument()),
                                    'xml': DocumentToXmlSerializerAdapter(MarkdownDocument()),
                                    'json': DocumentToJsonSerializerAdapter(MarkdownDocument()), }
        self.__themes: list[Theme] = [Theme(1, True, True), Theme(2, False, True),
                                      Theme(3, True, True), Theme(4, False, True),
                                      Theme(5, True, True), ]
        self.__settings: EditorSettings = EditorSettings()
        self.__doc: MarkdownDocument | None = None
        self.__current_user: User | None = None

    def _user_command(self, command: ICommand):
        self._check_can_edit_text()
        command.execute()
        self.__history.add_command(command)

    def user_message(self) -> str:
        return self.__current_user.message

    @property
    def settings(self) -> EditorSettings:
        return self.__settings

    def create_document(self) -> str:
        self.__current_user = Admin()
        self.__doc = MarkdownDocument()
        self.__doc.attach(self.__current_user)
        password = PasswordManager.create_password()
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
        docs = {'md': self.__doc, 'rtf': MdToRichTextAdapter(self.__doc), 'txt': MdToPlainTextAdapter(self.__doc)}

        if extension not in docs:
            raise Exception('Unknown extension')

        saver.save(docs[extension], filepath, serializer, extension=file_extension)

    def login_as_admin(self,
                       password: str):
        if self.__doc.validate_password(password):
            self.__doc.detach(self.__current_user)
            self.__current_user = Admin()
            self.__doc.attach(self.__current_user)
        else:
            raise Exception('Invalid password')

    def undo(self):
        try:
            self.__history.undo()
        except Exception:
            pass

    def redo(self):
        try:
            self.__history.redo()
        except Exception:
            pass

    def insert_text(self,
                    text: str,
                    position: int) -> None:
        self._user_command(WriteCommand(text, position, self.__doc))

    def erase_text(self,
                   start: int,
                   end: int) -> None:
        self._user_command(EraseCommand(start, end, self.__doc))

    def apply_style(self,
                    start: int,
                    end: int,
                    italic: bool = False,
                    strikethrough: bool = False,
                    bold: bool = False):
        self._user_command(ChangeStyleCommand(start, end, self.__doc, italic=italic,
                                              strikethrough=strikethrough, bold=bold))

    def set_theme(self,
                  theme_number: int):
        self._user_command(ChangeThemeCommand(self.__doc, self.__themes[theme_number - 1]))

    def read_only(self) -> bool:
        return self.__doc.settings.read_only

    def set_read_only(self,
                      read_only: bool):
        if not self.__current_user.can_change_document_settings():
            raise Exception('User cant change document settings')

        self.__doc.settings.read_only = read_only

    def get_text(self) -> str | None:
        return self.__doc.get_text() if self.__doc else None

    def is_opened(self) -> bool:
        return self.__doc is not None

    def _check_can_edit_text(self) -> None:
        if not self.__current_user.can_edit_text():
            raise Exception('User cant edit text')

    @staticmethod
    def delete_document(path: str, local=True) -> None:
        deleter = LocalFileManager if local else DatabaseFileManager
        deleter.delete(path)
