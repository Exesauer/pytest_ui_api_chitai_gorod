# pytest_ui_api_chitai_gorod

## Автоматизация тестирования для проекта "Читай-город" на Python

### Шаги
1. Создать виртуальное окружение `python -m venv venv`
2. Активировать виртуальное окружение:
   - Для Windows:
    `venv\Scripts\activate`
   - Для macOS/Linux:
    `source venv/bin/activate`
3. Склонировать проект: `git clone https://github.com/Exesauer/pytest_ui_api_chitai_gorod.git`
4. Установить все зависимости: `pip install -r requirements.txt`
5. Запустить тесты: `pytest`
6. Сгенерировать отчет: `allure generate allure-results --clean -o allure-report`
7. Открыть отчет: `allure open allure-report`

### Стек:
- **pytest**: Библиотека для написания и выполнения тестов.
- **selenium**: Инструмент для автоматизации веб-приложений в различных браузерах.
- **webdriver-manager**: Управляет установкой и обновлением драйверов для различных браузеров, автоматизируя этот процесс.
- **requests**: Библиотека для HTTP-запросов, полезна для API-тестов.
- **allure**: Фреймворк для генерации наглядных отчетов Allure на основе тестов Pytest.
- **configparser**: Для работы с конфигурациями проекта, обеспечивает гибкость и удобство настройки тестирования.

### Структура:
- ./tests - Тесты
- ./pages - Описание страниц
- ./api - Вспомогательные модули для работы с API
- ./configuration - Провайдер настроек для тестов
    - test_config.ini - Файл с настройками
- ./testdata - Провайдер тестовых данных
    - test_data.json - Файл с данными
- pytest.ini - Файл с настройками pytest

### Полезные ссылки
- [Подсказка по markdown](https://www.markdownguide.org/basic-syntax/)
- [Генератор файла .gitignore](https://www.toptal.com/developers/gitignore)
- [Официальный репозиторий библиотек Python](https://pypi.org/)
- [ConfigParser](https://docs.python.org/3/library/configparser.html)
- [pip freeze](https://pip.pypa.io/en/stable/cli/pip_freeze/)