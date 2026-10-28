import pytest

from page_loader.names import (
    to_page_filename,
    to_resource_filename,
    to_resources_dirname,
)


@pytest.mark.parametrize(
    ("url", "expected"),
    [
        ("https://ru.hexlet.io/courses", "ru-hexlet-io-courses.html"),
        ("https://ru.hexlet.io/courses/", "ru-hexlet-io-courses.html"),
        ("http://site.com", "site-com.html"),
    ],
)
def test_page_filename(url, expected):
    assert to_page_filename(url) == expected


def test_resources_dirname():
    url = "https://ru.hexlet.io/courses"
    assert to_resources_dirname(url) == "ru-hexlet-io-courses_files"


@pytest.mark.parametrize(
    ("url", "expected"),
    [
        (
            "https://ru.hexlet.io/assets/app.min.css",
            "ru-hexlet-io-assets-app-min.css",
        ),
        ("https://ru.hexlet.io/photo.png?v=2", "ru-hexlet-io-photo.png"),
        ("https://ru.hexlet.io/courses", "ru-hexlet-io-courses.html"),
    ],
)
def test_resource_filename_keeps_extension(url, expected):
    assert to_resource_filename(url) == expected
