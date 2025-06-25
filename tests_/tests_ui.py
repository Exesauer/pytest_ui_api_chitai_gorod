import pytest
import allure
import random
from configuration.ConfigProvider import ConfigProvider

base_url = ConfigProvider().get("ui", "base_url")


@pytest.mark.positive
@allure.epic("Интернет-магазин «Читай-город»")
@allure.feature("Тестовые сценарии UI")
@allure.severity("CRITICAL")
@allure.suite("UI: Позитивные тесты основного функционала магазина")
class TestPositive:
    """
    Класс для проведения позитивных UI-тестов основного функционала интернет-магазина «Читай-город».

    В рамках тестов этого класса проверяются стандартные сценарии использования магазина —
    такие как авторизация, навигация по разделам, поиск товаров, добавление товаров в корзину
    и другие повседневные операции, которые должен выполнять пользователь.
    Все тесты написаны для подтверждения корректной работы ключевых функций UI.
    """
    @pytest.fixture(autouse=True)
    def setup_class(
            self,
            browser,
            authorization,
            navigation,
            search,
            cart,
            product_dictionary):
        """
        Инициализирует объекты для тестирования.

        :param browser: Объект браузера.
        :param authorization: Объект для авторизации.
        :param navigation: Объект для навигации.
        :param search: Объект страницы поиска.
        :param cart: Объект страницы корзины.
        :param product_dictionary: Данные для проверки поиска.
        """
        self.browser = browser
        self.navigation = navigation
        self.authorization = authorization
        self.search = search
        self.cart = cart
        self.product_dictionary = product_dictionary

    @allure.story("Функциональность авторизации")
    @allure.title("Проверка авторизации пользователя")
    def test_login_with(self):
        autorizarition = self.authorization.login_with()

        with allure.step("Проверка корректного отображения имени пользователя"):
            assert autorizarition, "Ожидаемое имя пользователя не отобразилось"

    @allure.story("Функциональность навигации")
    @allure.title("Проверка перехода в личный профиль")
    def test_go_profile(self, add_cookies):
        go_profile = self.navigation.go_profile()

        with allure.step("Проверка корректности URL профиля"):
            assert go_profile.endswith(".ru/profile")

    @allure.story("Функциональность навигации")
    @allure.title("Проверка перехода в заказы")
    def test_go_orders(self, add_cookies):
        go_orders = self.navigation.go_orders()

        with allure.step("Проверка корректности URL заказов"):
            assert go_orders.endswith(".ru/profile/orders")

    @allure.story("Функциональность навигации")
    @allure.title("Проверка перехода в закладки")
    def test_go_bookmarks(self, add_cookies):
        go_bookmarks = self.navigation.go_bookmarks()

        with allure.step("Проверка корректности URL закладок"):
            assert go_bookmarks.endswith(".ru/profile/bookmarks")

    @allure.story("Функциональность навигации")
    @allure.title("Проверка перехода в корзину без токена авторизации")
    def test_go_cart(self):
        go_cart = self.navigation.go_cart()

        with allure.step("Проверка корректности URL корзины"):
            assert go_cart.endswith(".ru/cart")

    @allure.story("Функциональность навигации")
    @allure.title("Проверка перехода на главную страницу из основных разделов")
    def test_go_main(self, add_cookies):
        urls = []

        self.navigation.go_profile()
        urls.append(self.navigation.go_main())
        self.navigation.go_orders()
        urls.append(self.navigation.go_main())
        self.navigation.go_bookmarks()
        urls.append(self.navigation.go_main())
        self.navigation.go_cart()
        urls.append(self.navigation.go_main())

        with allure.step("Проверка корректности URL главной страницы"):
            assert all(
                url == base_url for url in urls), "Не все переходы привели на главную страницу"

    @allure.story("Функциональность поиска товаров")
    @allure.title("Проверка корректности результатов поиска товаров")
    def test_validate_search_results(self):
        title_1, title_2 = random.choice(
            list(self.product_dictionary.items()))

        self.search.search_products(title_1)
        self.search.validate_search_results([title_1, title_2])

        self.browser.refresh()

    @allure.story("Верификация данных о товарах")
    @allure.title("Сравнение названий товаров из результатов поиска с названиями на их страницах")
    def test_compare_search(self):
        title_1, _ = random.choice(list(self.product_dictionary.items()))

        self.search.search_products(title_1)
        self.search.compare_search_and_product_titles(5)

        self.browser.get(base_url)

    @allure.story("Функциональность корзины")
    @allure.title("Проверка очистки корзины")
    def test_clear_cart(self):
        title_1, _ = random.choice(list(self.product_dictionary.items()))
        count = 5
        self.search.search_products(title_1)
        self.cart.add_products_to_cart(count)
        self.navigation.go_cart()
        self.cart.clear_cart()
        self.browser.refresh()

        with allure.step("Проверка очистки содержимого корзины"):
            assert self.cart.get_cart_items_count() == 0
        with allure.step("Проверка значения индикатора после очистки"):
            assert self.cart.get_indicator_value() == 0

    @allure.story("Функциональность корзины")
    @allure.title("Проверка добавления товаров в корзину из результатов поиска")
    def test_add_products_to_cart(self, api_clear_cart):
        title_1, _ = random.choice(list(self.product_dictionary.items()))
        count = 5

        self.search.search_products(title_1)
        self.cart.add_products_to_cart(count)
        self.navigation.go_cart()

        with allure.step("Проверка количества товаров в корзине"):
            assert self.cart.get_cart_items_count() == count
        with allure.step("Проверка значения индикатора корзины"):
            assert self.cart.get_indicator_value() == count

        self.cart.clear_cart()

    @allure.story("Функциональность корзины")
    @allure.title("Проверка соответствия итоговой суммы в корзине и на этапе заказа")
    def test_total_amount(self, add_cookies):
        title_1, _ = random.choice(list(self.product_dictionary.items()))

        self.search.search_products(title_1)
        self.cart.add_products_to_cart(5)
        self.navigation.go_cart()
        amount_cart = self.cart.total_amount_cart()
        self.cart.go_checkout()
        amount_order = self.cart.total_amount_order()

        with allure.step("Проверка соответствия суммы в корзине и на этапе заказа"):
            assert amount_cart == amount_order


@pytest.mark.negative
@allure.epic("Интернет-магазин «Читай-город»")
@allure.feature("Тестовые сценарии UI")
@allure.severity("NORMAL")
@allure.suite("UI: Негативные тесты основного функционала магазина")
class TestNegative:
    """
    Класс для проведения негативных UI-тестов основного функционала интернет-магазина «Читай-город».

    В данных тестах проверяются ситуации, когда неавторизованный пользователь пытается
    получить доступ к функциональным разделам сайта, которые требуют авторизации:
    профиль, заказы, закладки, и оформление заказа. Тесты направлены на гарантирование,
    что пользователю отображается модальное окно аутентификации при попытке
    осуществления действий, требующих авторизации.
    """
    @pytest.fixture(autouse=True)
    def setup_class(
            self,
            browser,
            navigation,
            search,
            cart,
            product_dictionary):
        """
        Инициализирует объекты для тестирования.

        :param browser: Объект браузера.
        :param navigation: Объект для навигации.
        :param search: Объект страницы поиска.
        :param cart: Объект страницы корзины.
        :param product_dictionary: Данные для проверки поиска
        """
        self.browser = browser
        self.navigation = navigation
        self.search = search
        self.cart = cart
        self.product_dictionary = product_dictionary

    @allure.story("Функциональность навигации")
    @allure.title("Проверка перехода неавторизованного пользователя в разделы, которые требуют авторизации")
    def test_go_section_unauth(self):
        self.browser.delete_all_cookies()
        self.browser.refresh()
        go_profile = self.navigation.go_section_unauth("profile")
        self.browser.refresh()
        go_orders = self.navigation.go_section_unauth("orders")
        self.browser.refresh()
        go_bookmarks = self.navigation.go_section_unauth("bookmarks")
        self.browser.refresh()

        with allure.step("Проверка отображения модального окна аутентификации при переходе в профиль"):
            assert go_profile, "Модальное окно аутентификации не отобразилось."

        with allure.step("Проверка отображения модального окна аутентификации при переходе в заказы"):
            assert go_orders, "Модальное окно аутентификации не отобразилось."

        with allure.step("Проверка отображения модального окна аутентификации при переходе в закладки"):
            assert go_bookmarks, "Модальное окно аутентификации не отобразилось."

    @allure.story("Функциональность корзины")
    @allure.title("Проверка перехода неавторизованного пользователя к процессу оформления заказа")
    def test_go_checkout_unauth(self):
        self.browser.delete_all_cookies()
        self.browser.refresh()
        title_1, _ = random.choice(list(self.product_dictionary.items()))

        self.search.search_products(title_1)
        self.cart.add_products_to_cart(5)
        self.navigation.go_cart()

        with allure.step("Проверка отображения модального окна аутентификации при переходе к процессу оформления заказа"):
            assert self.cart.go_checkout_unauth(), "Модальное окно аутентификации не отобразилось."