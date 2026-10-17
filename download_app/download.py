import requests
from download_app import exceptions as exceptions
from pathlib import Path

import logging

logging.basicConfig(level=logging.DEBUG)

def download_file(url, file_name="latest.txt"):
    logging.info(f"Próba pobrania zasobu: {url}")
    folder = Path.home() / "Downloads"
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / file_name
    logging.info(f"Ścieżka zapisu: {path}")
    with requests.get(url, stream=True, timeout=10) as response:
        if response.status_code == 404:
            raise exceptions.NotFoundError(f"Nie znaleziono zasobu (404): {url}")
        if response.status_code == 403:
            raise exceptions.AccessDeniedError(f"Brak dostępu (403): {url}")
        response.raise_for_status()

        with open(path, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)

    logging.info(f"Zapisano plik: {file_name}, {path}")
    return path