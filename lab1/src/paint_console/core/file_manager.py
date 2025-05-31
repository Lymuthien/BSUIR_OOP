import pickle


class FileManager:
    @staticmethod
    def save(data, filename: str) -> None:
        """Save data to file"""
        try:
            serialized_data = pickle.dumps(data)
            with open(filename, "wb") as f:
                f.write(serialized_data)
        except Exception as e:
            raise Exception(f"Save failed: {str(e)}")

    @staticmethod
    def load(filename: str):
        """Load data from file"""
        try:
            with open(filename, "rb") as f:
                serialized_data = pickle.loads(f.read())
                return serialized_data
        except FileNotFoundError:
            raise FileNotFoundError(f"File {filename} does not exist")
        except Exception as e:
            raise Exception(f"Load failed: {str(e)}")
