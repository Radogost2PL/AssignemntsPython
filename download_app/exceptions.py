class DownloadError(Exception):
    """Bazowy wyjątek dla błędów pobierania."""


class NotFoundError(DownloadError):
    """Serwer zwrócił kod 404."""


class AccessDeniedError(DownloadError):
    """Serwer zwrócił kod 403."""