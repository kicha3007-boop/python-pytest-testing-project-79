"""Имена файлов из адресов: ru.hexlet.io/courses → ru-hexlet-io-courses."""

import os
import re
from urllib.parse import urlparse

NOT_ALNUM = re.compile(r"[^a-zA-Z0-9]")
PAGE_EXTENSION = ".html"
RESOURCES_SUFFIX = "_files"


def to_name(url: str) -> str:
    """Адрес без схемы, всё кроме букв и цифр заменено дефисом."""
    parsed = urlparse(url)
    address = f"{parsed.netloc}{parsed.path}".rstrip("/")
    return NOT_ALNUM.sub("-", address)


def to_page_filename(url: str) -> str:
    return to_name(url) + PAGE_EXTENSION


def to_resources_dirname(url: str) -> str:
    return to_name(url) + RESOURCES_SUFFIX


def to_resource_filename(url: str) -> str:
    """Расширение ресурса сохраняется, у ресурса без расширения — .html."""
    parsed = urlparse(url)
    root, extension = os.path.splitext(parsed.path)
    name = to_name(parsed._replace(path=root).geturl())
    return name + (extension or PAGE_EXTENSION)
