from pathlib import Path

import pytest

FIXTURES = Path(__file__).parent / "fixtures"

PAGE_URL = "https://ru.hexlet.io/courses"
RESOURCES_DIR = "ru-hexlet-io-courses_files"

# Локальные ресурсы страницы: адрес, фикстура с содержимым, имя файла.
RESOURCES = [
    (
        "https://ru.hexlet.io/assets/professions/python.png",
        "python.png",
        "ru-hexlet-io-assets-professions-python.png",
    ),
    (
        "https://ru.hexlet.io/assets/application.css",
        "application.css",
        "ru-hexlet-io-assets-application.css",
    ),
    (
        "https://ru.hexlet.io/packs/js/runtime.js",
        "runtime.js",
        "ru-hexlet-io-packs-js-runtime.js",
    ),
    (PAGE_URL, "page.html", "ru-hexlet-io-courses.html"),
]


def read_fixture(name: str, mode: str = "r"):
    encoding = None if "b" in mode else "utf-8"
    with open(FIXTURES / name, mode, encoding=encoding) as file:
        return file.read()


@pytest.fixture
def site(requests_mock):
    """Сайт с одной страницей и её ресурсами; сеть подменена."""
    requests_mock.get(PAGE_URL, text=read_fixture("page.html"))
    for url, fixture, _ in RESOURCES[:-1]:
        requests_mock.get(url, content=read_fixture(fixture, "rb"))
    return requests_mock
