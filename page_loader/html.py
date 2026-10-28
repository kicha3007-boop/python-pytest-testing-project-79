"""Разбор страницы без побочных эффектов: локальные ресурсы и новые ссылки."""

import posixpath
from dataclasses import dataclass
from urllib.parse import urljoin, urlparse

from bs4 import BeautifulSoup

from page_loader.names import to_resource_filename, to_resources_dirname

# Какой атрибут у какого тега указывает на ресурс.
RESOURCE_ATTRIBUTES = {"img": "src", "link": "href", "script": "src"}


@dataclass(frozen=True)
class Resource:
    url: str
    relative_path: str  # путь от директории страницы


def prepare_page(html: str, page_url: str) -> tuple[str, list[Resource]]:
    """Возвращает HTML со ссылками на локальные копии и список ресурсов.

    Локальный ресурс — с того же хоста, что и страница; чужие не трогаются.
    """
    soup = BeautifulSoup(html, "html.parser")
    resources_dir = to_resources_dirname(page_url)
    page_host = urlparse(page_url).netloc
    resources = []

    for tag_name, attribute in RESOURCE_ATTRIBUTES.items():
        for tag in soup.find_all(tag_name, attrs={attribute: True}):
            url = urljoin(page_url, tag[attribute])
            if urlparse(url).netloc != page_host:
                continue
            # Ссылка в HTML — всегда со слешем, независимо от ОС.
            relative_path = posixpath.join(
                resources_dir, to_resource_filename(url)
            )
            tag[attribute] = relative_path
            resources.append(Resource(url, relative_path))

    return soup.prettify(), resources
