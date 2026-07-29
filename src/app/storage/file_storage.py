from pathlib import Path


class FileStorage:
    def __init__(
        self,
        base_path: Path,
    ):
        self.base_path = base_path

    async def save(
        self,
        name: str,
        content: bytes,
    ) -> str:
        """Сохранить файл в хранилище и вернуть путь к нему."""
        path = self.base_path / name

        path.write_bytes(content)

        return str(path)
