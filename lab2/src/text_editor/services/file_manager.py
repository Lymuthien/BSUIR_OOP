import io
import os

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload, MediaIoBaseUpload

from ..interfaces import ISerializer, IFileManager


class LocalFileManager(IFileManager):
    def save(self,
             data,
             filename: str,
             serializer: ISerializer,
             extension: str = None) -> None:
        serialized_data = serializer.serialize(data)
        filename += '.'
        filename += serializer.extension if extension is None else extension

        with open(filename, 'w') as file:
            file.write(serialized_data)

    def load(self,
             filename: str,
             serializer: ISerializer):
        with open(filename, 'r') as file:
            serialized_data = file.read()

        return serializer.deserialize(serialized_data)

    def delete(self,
               path: str) -> None:
        try:
            os.remove(path)
        except Exception:
            raise


class GoogleDriveFileManager(IFileManager):
    def __init__(self,
                 credentials_path: str):
        self.__credentials = service_account.Credentials.from_service_account_file(credentials_path)
        self.__service = build('drive', 'v3', credentials=self.__credentials)

    def save(self,
             data,
             filename: str,
             serializer: ISerializer,
             extension: str = None) -> None:
        serialized_data = serializer.serialize(data)
        filename += '.'
        filename += serializer.extension if extension is None else extension

        file_stream = io.BytesIO(serialized_data.encode('utf-8'))

        file_metadata = {
            'name': filename,
            'parents': ['1DAB9l237n3EXJ71uHHZm06ZY9jAqOCMB']
        }
        media = MediaIoBaseUpload(file_stream, mimetype='text/plain')
        self.__service.files().create(body=file_metadata, media_body=media, fields='id').execute()

    def load(self,
             filename: str,
             serializer: ISerializer):
        results = self.__service.files().list(q=f"name='{filename}'", fields="files(id)").execute()
        items = results.get('files', [])

        if not items:
            raise FileNotFoundError(f"Файл {filename} не найден")

        file_id = items[0]['id']
        request = self.__service.files().get_media(fileId=file_id)
        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while not done:
            status, done = downloader.next_chunk()

        fh.seek(0)
        serialized_data = fh.read().decode()
        return serializer.deserialize(serialized_data)

    def delete(self,
               path: str) -> None:
        results = self.__service.files().list(q=f"name='{path}'", fields="files(id)").execute()
        items = results.get('files', [])

        if not items:
            raise FileNotFoundError(f"Файл {path} не найден")

        file_id = items[0]['id']
        self.__service.files().delete(fileId=file_id).execute()
