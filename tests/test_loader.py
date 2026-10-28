import os

import pytest
import requests
from conftest import PAGE_URL, RESOURCES, RESOURCES_DIR, read_fixture

from page_loader import download
from page_loader.errors import NetworkError, StorageError


def test_download_saves_page_and_resources(site, tmp_path):
    file_path = download(PAGE_URL, str(tmp_path))

    assert file_path == str(tmp_path / "ru-hexlet-io-courses.html")
    with open(file_path, encoding="utf-8") as file:
        assert file.read() == read_fixture("expected.html")

    assert sorted(os.listdir(tmp_path / RESOURCES_DIR)) == sorted(
        name for _, _, name in RESOURCES
    )
    for _, fixture, name in RESOURCES:
        saved = (tmp_path / RESOURCES_DIR / name).read_bytes()
        assert saved == read_fixture(fixture, "rb"), name


def test_download_to_current_directory(site, tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    file_path = download(PAGE_URL)

    assert os.path.samefile(file_path, tmp_path / "ru-hexlet-io-courses.html")


def test_external_resources_are_not_requested(site, tmp_path):
    download(PAGE_URL, str(tmp_path))

    hosts = {request.netloc for request in site.request_history}
    assert hosts == {"ru.hexlet.io"}


@pytest.mark.parametrize("status", [404, 500])
def test_page_http_error(requests_mock, tmp_path, status):
    requests_mock.get(PAGE_URL, status_code=status)

    with pytest.raises(NetworkError, match=str(status)):
        download(PAGE_URL, str(tmp_path))
    assert os.listdir(tmp_path) == []


def test_page_network_error(requests_mock, tmp_path):
    requests_mock.get(PAGE_URL, exc=requests.ConnectionError("refused"))

    with pytest.raises(NetworkError, match=f"Failed to download {PAGE_URL}"):
        download(PAGE_URL, str(tmp_path))
    assert os.listdir(tmp_path) == []


def test_resource_http_error(site, tmp_path):
    site.get("https://ru.hexlet.io/assets/application.css", status_code=404)

    with pytest.raises(NetworkError, match="application.css"):
        download(PAGE_URL, str(tmp_path))


def test_missing_output_directory(site, tmp_path):
    missing = tmp_path / "missing"

    with pytest.raises(StorageError, match="does not exist"):
        download(PAGE_URL, str(missing))
    assert not missing.exists(), "директория не создаётся сама"


def test_output_is_a_file(site, tmp_path):
    file = tmp_path / "file.txt"
    file.write_text("")

    with pytest.raises(StorageError, match="does not exist"):
        download(PAGE_URL, str(file))


def test_resources_directory_is_blocked_by_file(site, tmp_path):
    (tmp_path / RESOURCES_DIR).write_text("")

    with pytest.raises(StorageError, match="Cannot create directory"):
        download(PAGE_URL, str(tmp_path))


@pytest.mark.skipif(
    os.name == "nt" or os.geteuid() == 0,
    reason="права на запись проверяются только не от root и не на Windows",
)
def test_output_without_write_permission(site, tmp_path):
    readonly = tmp_path / "readonly"
    readonly.mkdir(mode=0o555)

    with pytest.raises(StorageError, match="Cannot"):
        download(PAGE_URL, str(readonly))
