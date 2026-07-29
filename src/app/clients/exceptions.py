class FileProviderError(Exception):
    """Базовая ошибка внешнего API."""


class FileProviderRateLimitError(FileProviderError):
    """Превышен лимит запросов."""

    def __init__(
        self,
        retry_after: int | None = None,
    ):
        self.retry_after = retry_after


class FileProviderBlockedError(FileProviderError):
    """Клиент временно заблокирован."""

    def __init__(
        self,
        retry_after: int | None = None,
    ):
        self.retry_after = retry_after

        super().__init__(
            "File provider blocked",
        )
