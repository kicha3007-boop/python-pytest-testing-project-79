from conftest import PAGE_URL, RESOURCES, RESOURCES_DIR, read_fixture

from page_loader.html import Resource, prepare_page


def test_rewrites_only_local_links():
    html, _ = prepare_page(read_fixture("page.html"), PAGE_URL)

    assert html == read_fixture("expected.html")
    assert "https://cdn2.hexlet.io/assets/menu.css" in html
    assert "https://js.stripe.com/v3/" in html
    assert 'href="/professions/python"' in html, "обычные ссылки не трогаются"


def test_lists_local_resources():
    _, resources = prepare_page(read_fixture("page.html"), PAGE_URL)

    expected = [
        Resource(url, f"{RESOURCES_DIR}/{name}") for url, _, name in RESOURCES
    ]
    assert sorted(resources, key=by_url) == sorted(expected, key=by_url)


def by_url(resource):
    return resource.url


def test_page_without_resources():
    html, resources = prepare_page("<p>text</p>", PAGE_URL)

    assert resources == []
    assert "text" in html
