from app.core.config import STORAGE_PATH
from app.storage.file_storage import FileStorage


def get_file_storage() -> FileStorage:
    return FileStorage(base_path=STORAGE_PATH)
