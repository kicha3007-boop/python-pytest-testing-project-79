"""Главная функция: скачать страницу, подготовить ресурсы, сохранить всё."""

import logging
import os

import requests

from page_loader.errors import NetworkError, StorageError
from page_loader.html import prepare_page
from page_loader.names import to_page_filename, to_resources_dirname

logger = logging.getLogger(__name__)

TIMEOUT_SECONDS = 30


def download(url: str, output: str | None = None) -> str:
    """Скачивает страницу с локальными ресурсами в существующую директорию.

    Без output — в текущую директорию. Возвращает полный путь к странице.
    """
    output = os.getcwd() if output is None else output
    ensure_directory(output)
    logger.debug("downloading %s to %s", url, output)

    html, resources = prepare_page(fetch(url).text, url)
    logger.debug("found %d local resources", len(resources))

    resources_dir = os.path.join(output, to_resources_dirname(url))
    if resources:
        make_directory(resources_dir)
    for resource in resources:
        content = fetch(resource.url).content
        save(os.path.join(output, resource.relative_path), content)

    page_path = os.path.join(output, to_page_filename(url))
    save(page_path, html.encode())
    logger.info("page %s saved as %s", url, page_path)
    return page_path


def ensure_directory(path: str) -> None:
    if not os.path.isdir(path):
        raise StorageError(f"Output directory does not exist: {path}")


def fetch(url: str) -> requests.Response:
    try:
        response = requests.get(url, timeout=TIMEOUT_SECONDS)
        response.raise_for_status()
    except requests.RequestException as error:
        raise NetworkError(f"Failed to download {url}: {error}") from error
    logger.debug("got %s (%d bytes)", url, len(response.content))
    return response


def make_directory(path: str) -> None:
    try:
        os.makedirs(path, exist_ok=True)
    except OSError as error:
        message = f"Cannot create directory {path}: {error}"
        raise StorageError(message) from error


def save(path: str, content: bytes) -> None:
    try:
        with open(path, "wb") as file:
            file.write(content)
    except OSError as error:
        raise StorageError(f"Cannot save {path}: {error}") from error
    logger.debug("saved %s", path)
