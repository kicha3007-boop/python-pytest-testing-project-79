class PageLoaderError(Exception):
    """Общая ошибка загрузчика: её ловит командная часть."""


class NetworkError(PageLoaderError):
    """Страница или ресурс не скачались: сеть или ответ не 2xx."""


class StorageError(PageLoaderError):
    """Не удалось сохранить: нет директории, нет прав, путь — не директория."""
