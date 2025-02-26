import json
import os


class FileManager:
    @staticmethod
    def save(data, filename: str) -> None:
        try:
            serialized_data = json.dumps(data)
            with open(filename, 'w') as f:
                f.write(serialized_data)
        except Exception as e:
            raise FileManagerError(f"Save failed: {str(e)}")

    @staticmethod
    def load(filename: str):
        if not os.path.exists(filename):
            raise FileNotFoundError(f"File {filename} does not exist")

        try:
            with open(filename, 'r') as f:
                serialized_data = json.loads(f.read())
                return json.loads(serialized_data)
        except Exception as e:
            raise FileManagerError(f"Load failed: {str(e)}")


class FileManagerError(Exception):
    pass
