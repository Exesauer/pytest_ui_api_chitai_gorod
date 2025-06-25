# pytest_ui_api_chitai_gorod

# Автоматизация тестирования для проекта «Читай-город» на Python

# Шаги
1. Создать виртуальное окружение: `python - m venv venv`
    - Python должен быть установлен и добавлен в PATH системы.
2. Активировать виртуальное окружение:
    - Для Windows(Command Prompt): `venv\Scripts\activate.bat`
    - Для Windows (PowerShell): `venv\Scripts\Activate.ps1`
    - Для macOS/Linux: `source venv/bin/activate`

3. Склонировать проект с GitHub: `git clone https://github.com/Exesauer/pytest_ui_api_chitai_gorod.git`
4. Установить все необходимые зависимости: `pip install -r requirements.txt`
    > Совет: Если возникнут ошибки, необходимо проверить совместимость версий в requirements.txt и обновить пакеты.
5. Перейти на сайт https://www.chitai-gorod.ru/ и выполнить вход с использованием номера телефона.
6. Заполнить файл с тестовыми данными: test_data.json. 
    - "username": "Имя, отображаемое в иконке профиля",
    - "phone": "+7...",
    - "token": "Bearer ... DevTools-Application-Cookies: (access-token)"
    > Примечание: Токен действителен в течение одного часа. Используйте инструменты разработчика в браузере, чтобы получить его.
7. Запустить все тесты: `pytest`
    - только UI-тесты: `pytest ./tests_/tests_ui.py`
    - только API-тесты: `pytest ./tests_/tests_api.py`
    > Совет: Если pytest не установлен: `pip install pytest`
8. Сгенерировать с помощью Allure: `allure generate allure-results --clean -o allure-report`
   > Примечание: Убедитесь, что у вас установлен Allure. Установку Allure можно найти в официальной документации.
9. Открыть отчет в браузере: `allure open allure-report`

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