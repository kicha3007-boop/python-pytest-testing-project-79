# Тестирование загрузчика страниц (Python)

[![hexlet-check](https://github.com/kicha3007-boop/python-pytest-testing-project-79/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/kicha3007-boop/python-pytest-testing-project-79/actions)
[![CI](https://github.com/kicha3007-boop/python-pytest-testing-project-79/actions/workflows/ci.yml/badge.svg)](https://github.com/kicha3007-boop/python-pytest-testing-project-79/actions/workflows/ci.yml)

`page-loader` — утилита и библиотека: скачивает страницу вместе с локальными ресурсами (картинки, стили,
скрипты, ссылки `link` с того же хоста) и переписывает ссылки на скачанные файлы, чтобы страница открывалась
без сети. Главное в проекте — тесты: сеть подменена `requests-mock`, каждый тест — в своей временной директории.

## Установка

Нужен [uv](https://docs.astral.sh/uv/) (Python 3.12+ он поставит сам).

```bash
git clone https://github.com/kicha3007-boop/python-pytest-testing-project-79.git
cd python-pytest-testing-project-79
make install          # зависимости
make test             # тесты
make test-coverage    # тесты с порогом покрытия 95%
make lint             # ruff
make build package-install   # команда page-loader в системе
```

## Использование

```bash
page-loader --output /var/tmp https://ru.hexlet.io/courses
Page was downloaded as '/var/tmp/ru-hexlet-io-courses.html'

page-loader --log-level DEBUG https://ru.hexlet.io/courses   # отладочный лог в stderr
```

- `-o, --output` — куда сохранять, директория должна существовать (по умолчанию текущая);
- `--log-level` (или переменная `PAGE_LOADER_LOG_LEVEL`) — уровень лога в stderr, по умолчанию `WARNING`;
- страница: `ru-hexlet-io-courses.html`, ресурсы: `ru-hexlet-io-courses_files/ru-hexlet-io-assets-application.css` —
  адрес без схемы, всё кроме букв и цифр заменено на `-`, расширение сохраняется (у страниц — `.html`);
- ресурсы с других хостов не скачиваются и их ссылки не меняются;
- ошибки (ответ не 2xx, сеть, нет директории, нет прав) — сообщение в stderr и код выхода `1`.

Как библиотека:

```python
from page_loader import download

file_path = download('https://ru.hexlet.io/courses', '/var/tmp')
```

Ошибки: `page_loader.errors.NetworkError` (страница или ресурс не скачались) и `StorageError`
(не удалось сохранить); обе наследуют `PageLoaderError`.

## Устройство

- `page_loader/loader.py` — пайплайн: проверить директорию, скачать страницу, подготовить ресурсы, сохранить;
- `page_loader/html.py` — разбор HTML без побочных эффектов: локальные ресурсы и новые ссылки;
- `page_loader/names.py` — имена файлов и директории из адреса;
- `page_loader/cli.py` — командная часть: аргументы, вывод, коды возврата.

Тесты: `tests/test_html.py` и `tests/test_names.py` — разбор и имена без сети, `tests/test_loader.py` — загрузка
с подменённой сетью и ошибки, `tests/test_cli.py` — вывод и коды возврата. Фикстуры — `tests/fixtures/`.
