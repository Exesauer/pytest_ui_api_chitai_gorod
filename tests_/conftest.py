import pytest
import allure
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from configuration.ConfigProvider import ConfigProvider
from UI.authorization import Authorization
from UI.cart_page import CartPage
from UI.search_page import SearchPage
from UI.navigation import Navigation
from API.cart_api import CartApi
from testdata.DataProvider import DataProvider


@pytest.fixture(scope="session")
def browser():
    """
    **Фикстура для инициализации и завершения работы веб-браузера.**

    Запускает браузер (Chrome или Firefox), настраивает его и открывает указанный URL.
    Устанавливает имплицитное ожидание и максимизирует окно браузера. По завершении всех тестов браузер закрывается.

       Браузер, URL сайта и имплицитное ожидание определяются с помощью класса ConfigProvider.
    """
    with allure.step("Открытие и настройка браузера"):
        if ConfigProvider().get("ui", "browser_name") == "Chrome":
            driver = webdriver.Chrome(service=Service(
                ChromeDriverManager().install()))
        else:
            driver = webdriver.Firefox(
                service=FirefoxService(GeckoDriverManager().install()))
        driver.get(ConfigProvider().get("ui", "base_url"))
        driver.implicitly_wait(ConfigProvider().get_int("ui", "timeout"))
        driver.maximize_window()

        yield driver

    with allure.step("Закрытие браузера"):
        driver.quit()


@pytest.fixture(scope="session")
def auth(browser) -> None:
    """
    Фикстура для авторизации на сайте.

    Использует объект Authorization для выполнения процесса входа.
    """
    base_page = Authorization(browser)
    base_page.login_with()


@pytest.fixture(scope="session")
def authorization(browser) -> Authorization:
    """Фикстура для предоставления объекта Authorization."""
    return Authorization(browser)


@pytest.fixture(scope="session")
def navigation(browser) -> Navigation:
    """Фикстура для предоставления объекта Navigation."""
    return Navigation(browser)


@pytest.fixture(scope="session")
def cart(browser) -> CartPage:
    """Фикстура для предоставления объекта CartPage."""
    return CartPage(browser)


@pytest.fixture(scope="session")
def search(browser) -> SearchPage:
    """Фикстура для предоставления объекта SearchPage."""
    return SearchPage(browser)


@pytest.fixture(scope="session")
def product_dictionary() -> dict:
    """
    Фикстура, возвращающая словарь с названиями товаров и их эквивалентами на другом языке.

    :return: dict: Словарь для тестирования поиска товаров с ключами на одном языке и значениями на другом.
    """
    product_dict = {
        "Harry Potter": "Гарри Поттер",
        "Властелин Колец": "The Lord of The Ring",
        "Diablo": "Диабло",
        "Ведьмак": "Witcher",
        "Warcraft": "Варкрафт",
        "Игра престолов": "Game of Thrones"
    }
    return product_dict


@pytest.fixture(scope="session")
def cart_api() -> CartApi:
    """Фикстура для предоставления объекта CartApi."""
    return CartApi()


@pytest.fixture(scope="function")
def api_clear_cart(browser, cart_api):
    """Фикстура, очищающая корзину через API.

    :param cart_api: объект CartApi для взаимодействия с корзиной.
    """
    cart_api.clear_cart()
    browser.refresh()


@pytest.fixture(scope="function")
def cart_item(cart_api):
    """Фикстура, добавляющая случайный продукт в корзину для тестирования.

    :param cart_api: объект CartApi для взаимодействия с корзиной.

    :return:
    Кортеж из идентификатора продукта и идентификатора продукта в корзине.

    После завершения теста удаляет продукт из корзины.
    """
    product_id = cart_api.get_random_id()
    cart_api.add_product_to_cart(product_id)
    cart_product_id = cart_api.get_product_in_cart(product_id).get("id")

    yield product_id, cart_product_id

    cart_api.delete_product_from_cart(cart_product_id)


@pytest.fixture(scope="session")
def add_cookies(browser):
    browser.add_cookie({
        "name": "access-token",
        "value": DataProvider().get("token"),
        'path': '/',
        'domain': 'chitai-gorod.ru',
    })
