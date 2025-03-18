import sqlite3
from ..interfaces import ISerializer, IFileManager


class LocalFileManager(IFileManager):
    @staticmethod
    def save(data, filename: str, serializer: ISerializer) -> None:
        serialized_data = serializer.serialize(data)
        filename += serializer.extension
        with open(filename, 'w') as file:
            file.write(serialized_data)

    @staticmethod
    def load(filename: str, serializer: ISerializer):
        with open(filename, 'r') as file:
            serialized_data = file.read()

        return serializer.deserialize(serialized_data)


class DatabaseFileManager(IFileManager):
    def __init__(self, db_name: str = 'documents.db'):
        self.__db_name = db_name
        self._create_table()

    @property
    def db_name(self) -> str:
        return self.__db_name

    def _create_table(self) -> None:
        with sqlite3.connect(self.__db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS documents (
                    id TEXT PRIMARY KEY,
                    data TEXT NOT NULL,
                    format TEXT NOT NULL
                )
            """)
            conn.commit()

    @staticmethod
    def save(data, document_id: str, serializer: ISerializer) -> None:
        db_manager = DatabaseFileManager()
        serialized_data = serializer.serialize(data)
        format_ = serializer.extension

        with sqlite3.connect(db_manager.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR REPLACE INTO documents (id, data, format)
                VALUES (?, ?, ?)
            """, (document_id, serialized_data, format_))
            conn.commit()

    @staticmethod
    def load(document_id: str, serializer: ISerializer):
        db_manager = DatabaseFileManager()

        with sqlite3.connect(db_manager.__db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT data, format FROM documents WHERE id = ?
            """, (document_id,))
            result = cursor.fetchone()

            if result is None:
                raise ValueError

            serialized_data, stored_format = result
            if stored_format != serializer.extension:
                raise ValueError

            return serializer.deserialize(serialized_data)
