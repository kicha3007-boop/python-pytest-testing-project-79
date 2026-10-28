from conftest import PAGE_URL

from page_loader.cli import main


def test_prints_path_and_returns_zero(site, tmp_path, capsys):
    code = main(["-o", str(tmp_path), PAGE_URL])

    assert code == 0
    out, err = capsys.readouterr()
    assert str(tmp_path / "ru-hexlet-io-courses.html") in out
    assert err == ""


def test_error_goes_to_stderr_with_nonzero_code(site, tmp_path, capsys):
    code = main(["-o", str(tmp_path / "missing"), PAGE_URL])

    assert code == 1
    out, err = capsys.readouterr()
    assert out == ""
    assert "does not exist" in err
