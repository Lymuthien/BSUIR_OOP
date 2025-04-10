from .auth_service import AuthService
from .history_manager import HistoryManager
from ..factories.document_factory import MDFactory, DocumentFactory
from ..factories.user_factory import users, AdminUserFactory, UserFactory
from ..interfaces import ICommand, IFileManager, ISerializer
from ..models import ChangeStyleCommand, WriteCommand, EraseCommand, ChangeThemeCommand, MarkdownDocument, \
    MdToRichTextAdapter, MdToPlainTextAdapter, Theme, EditorSettings


class Editor(object):
    def __init__(self, serializers: dict[str, ISerializer]):
        self.__users: list[str] = []
        self.__themes: list[Theme] = [Theme(1), Theme(2), Theme(3), Theme(4), Theme(5), ]
        self.__serializers: dict[str, ISerializer] = serializers
        self.__settings: EditorSettings = EditorSettings()
        self.__doc: MarkdownDocument | None = None
        self.__current_user: str | None = None
        self.__file_manager: IFileManager | None = None
        self.__document_factory: DocumentFactory = MDFactory()
        self.__user_factory: UserFactory = AdminUserFactory()

        self.__auth_service = AuthService(self.__users)
        self.__history: HistoryManager = HistoryManager()

    def _user_command(self, command: ICommand):
        if self._is_user_can_edit_text():
            command.execute()
            self.__history.add_command(command)

    def user_message(self) -> str:
        return self.__doc.get_role(self.__current_user).message

    @property
    def settings(self) -> EditorSettings:
        return self.__settings

    def create_document(self) -> None:
        if self.__current_user is None:
            raise Exception('Login please.')

        self.__doc = self.__document_factory.create_document()
        self.__user_factory = AdminUserFactory()
        self.__doc.attach(self.__user_factory.create_user(self.__current_user))

    def open_document(self,
                      filename: str) -> None:
        if self.__current_user is None:
            raise Exception('Login please.')

        extension = filename.split('.')[-1].lower()

        try:
            serializer = self.__serializers[extension]
        except KeyError:
            raise Exception('Unknown format')

        doc = self.__file_manager.load(filename, serializer)

        if doc.get_role(self.__current_user) is None:
            raise PermissionError('You cant read this file.')

        self.__doc = doc

    def close_document(self):
        self.__doc = None
        self.__history.clear()

    def set_file_manager(self, file_manager: IFileManager):
        self.__file_manager = file_manager

    def save_document(self,
                      filepath: str,
                      extension: str = 'md',
                      format_: str = 'json', ):
        extension = extension.lower().strip()
        format_ = format_.lower().strip()

        try:
            serializer = self.__serializers[format_]
        except Exception:
            raise Exception('Unknown format')

        docs = {'md': self.__doc, 'rtf': MdToRichTextAdapter(self.__doc), 'txt': MdToPlainTextAdapter(self.__doc)}

        if extension not in docs:
            raise Exception('Unknown extension')

        self.__file_manager.save(docs[extension], filepath, serializer)

    def login(self,
              name: str):
        self.__current_user = self.__auth_service.login(name)

    def register(self,
                 name: str, ):
        self.__current_user = self.__auth_service.register_user(name)
        self.__users.append(self.__current_user)

    def logout(self):
        self.__current_user = None

    def give_role(self,
                  name: str,
                  role: str, ):
        if self.__current_user is None:
            raise Exception('Login please')

        if name not in self.__users:
            raise Exception('User not found')

        if not self.__doc.get_role(self.__current_user).can_change_document_settings():
            raise PermissionError('User cant change document settings')

        try:
            user_class = users[role.lower()]
            self.__user_factory = user_class
            self.__doc.set_role(self.__user_factory.create_user(name))
        except Exception as e:
            raise print(str(e))

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

    def get_text(self) -> str | None:
        return self.__doc.get_text() if self.__doc else None

    def is_opened(self) -> bool:
        return self.__doc is not None

    def _is_user_can_edit_text(self) -> bool:
        return self.__doc.get_role(self.__current_user).can_edit_text()

    def _is_user_can_edit_settings(self) -> bool:
        return self.__doc.get_role(self.__current_user).can_change_document_settings()

    def delete_document(self, filename: str) -> None:
        self.open_document(filename)
        if self._is_user_can_edit_settings():
            self.__file_manager.delete(filename)
        self.close_document()

    def read_only(self) -> bool:
        return not self._is_user_can_edit_text()
