import pytest
import allure
import time
from configuration.ConfigProvider import ConfigProvider


@pytest.fixture(scope="class", autouse=True)
def delay_between_tests():
    """
    Фикстура добавляет задержку после выполнения каждого теста в классах.

    Время задержки задается в конфигурации и определяется параметром "request_delay" в секции "api".
    """
    yield
    time.sleep(ConfigProvider().get_int("api", "request_delay"))


@pytest.mark.positive
@allure.epic("Интернет-магазин «Читай-город»")
@allure.feature("Тестовые сценарии API")
@allure.severity("CRITICAL")
@allure.suite("API: Позитивные тесты функционала корзины")
class TestCartPositive():
    """
    Тест-кейс содержит набор позитивных сценариев для проверки корректной работы функционала корзины
    (просмотр, добавление, удаление товаров, обновление количества и др.)
    """
    @pytest.fixture(autouse=True)
    def setup_class(self, cart_api) -> None:
        """
        Инициализирует API клиента для доступа к функционалу корзины.

        :param cart_api: Объект CartApi, предоставляющий методы для взаимодействия с корзиной.
        """
        self.cart_api = cart_api

    @allure.story("Функциональность корзины")
    @allure.title("Проверка отображения содержимого корзины")
    def test_view_cart_contents(self):
        """Тест проверяет наличие необходимых полей в содержимом корзины."""
        required_fields = {
            "addBonuses", "cost", "costGiftWrap", "costWithBonuses",
            "costWithSale", "disabledProducts", "discount", "gifts",
            "preorderProducts", "products", "promoCode", "weight"
        }

        view_cart_contents = self.cart_api.view_cart_contents()
        view_cart_contents_body = view_cart_contents.json()
        has_all_fields = self.cart_api.check_fields_in_body(
            view_cart_contents_body, required_fields)

        with allure.step("Проверка наличия всех требуемых полей"):
            assert has_all_fields, "Некоторых полей не хватает в JSON."

        with allure.step("Проверка статус-кода ответа"):
            assert view_cart_contents.status_code == 200

    @allure.story("Функциональность корзины")
    @allure.title("Проверка добавления товара в корзину")
    def test_add_product_to_cart(self):
        """Тест проверяет возможность добавления товара в корзину и соответствие ответа ожиданиям."""
        product_id = self.cart_api.get_random_id()
        products_before = self.cart_api.get_all_products_in_cart()
        add_product = self.cart_api.add_product_to_cart(product_id)
        products_after = self.cart_api.get_all_products_in_cart()
        cart_product_id = self.cart_api.get_product_in_cart(
            product_id).get("id")
        self.cart_api.delete_product_from_cart(cart_product_id)

        with allure.step("Проверка, что количество товаров в корзине увеличилось на 1"):
            assert len(products_after) - len(products_before) == 1

        with allure.step("Проверка статус-кода и пустоты тела ответа"):
            assert add_product.status_code == 200
            assert add_product.text == '', "Тело ответа не пустое"

    @allure.story("Управление товарами в корзине")
    @allure.title("Проверка удаления товара из корзины")
    def test_delete_product_from_cart(self, cart_item):
        """Тест проверяет возможность удаления товара из корзины и соответствие ответа ожиданиям."""
        product_id, cart_id = cart_item

        products_before = self.cart_api.get_all_products_in_cart()
        delete_product = self.cart_api.delete_product_from_cart(cart_id)
        products_after = self.cart_api.get_all_products_in_cart()

        with allure.step("Проверка, что количество товаров в корзине уменьшилось на 1"):
            assert len(products_after) - len(products_before) == -1

        with allure.step("Проверка, что товара больше нет в корзине"):
            assert self.cart_api.get_product_in_cart(product_id) is None

        with allure.step("Проверка статус-кода и пустоты тела ответа"):
            assert delete_product.status_code == 204
            assert delete_product.text == '', "Тело ответа не пустое"

    @allure.story("Функциональность корзины")
    @allure.title("Проверка очистки корзины")
    def test_clear_cart(self, cart_item):
        """Тест проверяет возможность очистки корзины."""
        clear_cart = self.cart_api.clear_cart()

        with allure.step("Проверяем, что корзина очищена"):
            assert self.cart_api.get_all_products_in_cart() == []

        with allure.step("Проверка статус-кода и пустоты тела ответа"):
            assert clear_cart.status_code == 204
            assert clear_cart.text == '', "Тело ответа не пустое"

    @allure.story("Управление товарами в корзине")
    @allure.title("Проверка изменения количества определённого товара в корзине")
    def test_update_quantity(self, cart_item):
        """Тест проверяет возможность изменения количества товара в корзине."""
        product_id, cart_product_id = cart_item
        inc_quant = 5
        dec_quant = 4

        get_quant_before_inc = self.cart_api.get_product_in_cart(
            product_id).get("quantity")
        increase_quantity = self.cart_api.update_quantity(
            cart_product_id, inc_quant)
        get_quant_after_inc = self.cart_api.get_product_in_cart(
            product_id).get("quantity")
        decrease_quantity = self.cart_api.update_quantity(
            cart_product_id, dec_quant)
        get_quant_after_dec = self.cart_api.get_product_in_cart(
            product_id).get("quantity")

        with allure.step("Проверка, что начальное количество товара равно 1"):
            assert get_quant_before_inc == 1

        with allure.step("Проверка, что статус-коды увеличения и уменьшения количества равны 200"):
            assert increase_quantity.status_code == 200
            assert decrease_quantity.status_code == 200

        with allure.step("Проверка, что количество товара после увеличения равно заданному"):
            assert get_quant_after_inc == inc_quant

        with allure.step("Проверка, что количество товара после уменьшения равно заданному"):
            assert get_quant_after_dec == dec_quant


@pytest.mark.negative
@allure.epic("Интернет-магазин «Читай-город»")
@allure.feature("Тестовые сценарии API")
@allure.severity("NORMAL")
@allure.suite("API: Негативные тесты функционала корзины")
class TestCartNegative():
    """
    Тест-кейс содержит набор негативных сценариев для проверки устойчивости API корзины.
    """
    @pytest.fixture(autouse=True)
    def setup_class(self, cart_api):
        """Инициализация API клиента для доступа к функционалу корзины."""
        self.cart_api = cart_api

    @allure.story("Функциональность корзины")
    @allure.title("Добавление товара с невалидным ID")
    def test_add_product_with_invalid_id(self):
        """
        Проверка обработки запроса на добавление товара с некорректным id.

        Тест валидирует ошибку, структуру ошибки и отсутствие изменений в корзине.
        """
        product_id = 0

        products_before = self.cart_api.get_all_products_in_cart()
        add_product = self.cart_api.add_product_to_cart(product_id)
        add_product_body = add_product.json()
        error_message = add_product_body["errors"][0]
        products_after = self.cart_api.get_all_products_in_cart()
        required_fields = {"code", "source", "status", "title"}
        has_all_fields = self.cart_api.check_fields_in_body(
            error_message, required_fields)

        with allure.step("Проверка структуры ошибки"):
            assert has_all_fields, "Некоторых полей не хватает в JSON."

        with allure.step("Содержание сообщения об ошибке"):
            assert error_message["title"] == "Значение недопустимо."

        with allure.step("Проверка отсутствия изменений в корзине"):
            assert len(products_before) == len(products_after)

        with allure.step("Проверка статус-кода ответа"):
            assert add_product.status_code == 422

    @allure.story("Управление товарами в корзине")
    @allure.title("Удаление отсутствующего в корзине товара")
    def test_remove_missing_product(self):
        """
        Проверка обработки запроса на удаление товара, который отсутствует в корзине.

        Тест валидирует ошибку, структуру ошибки и отсутствие изменений в корзине.
        """
        missing_id = self.cart_api.get_random_id()

        self.cart_api.add_product_to_cart(missing_id)
        cart_product_id = self.cart_api.get_product_in_cart(
            missing_id).get("id")
        self.cart_api.delete_product_from_cart(cart_product_id)
        products_before = self.cart_api.get_all_products_in_cart()
        delete_product = self.cart_api.delete_product_from_cart(
            cart_product_id)
        delete_product_body = delete_product.json()
        products_after = self.cart_api.get_all_products_in_cart()
        required_fields = {"message", "requestId"}
        has_all_fields = self.cart_api.check_fields_in_body(
            delete_product_body, required_fields)

        with allure.step("Проверка структуры ошибки"):
            assert has_all_fields, "Некоторых полей не хватает в JSON."

        with allure.step("Содержание сообщения об ошибке"):
            assert delete_product_body["message"] == "товар в корзине не найден"

        with allure.step("Проверка отсутствия изменений в корзине"):
            assert len(products_after) == len(products_before)

        with allure.step("Проверка статус-кода ответа"):
            assert delete_product.status_code == 404

    @allure.story("Управление товарами в корзине")
    @allure.title("Изменение количества определенного товара на отрицательное")
    def test_update_quantity_to_negative(self, cart_item):
        """
        Проверка обработки запроса измения количества товара в корзине на отрицательное значение.

        Тест валидирует ошибку, структуру ошибки и отсутствие изменений в корзине.
        """
        product_id, cart_product_id = cart_item
        quantity = -1

        get_quantity_before = self.cart_api.get_product_in_cart(
            product_id).get("quantity")
        update_quantity = self.cart_api.update_quantity(
            cart_product_id, quantity)
        update_quantity_body = update_quantity.json()
        get_quantity_after = self.cart_api.get_product_in_cart(
            product_id).get("quantity")
        required_fields = {"message", "requestId"}
        has_all_fields = self.cart_api.check_fields_in_body(
            update_quantity_body, required_fields)

        with allure.step("Проверка структуры ошибки"):
            assert has_all_fields, "Некоторых полей не хватает в JSON."

        with allure.step("Валидация отсутствия изменения количества товара"):
            assert get_quantity_before == get_quantity_after

        with allure.step("Ожидание кода ошибки 422"):
            assert update_quantity.status_code == 422

        with allure.step("Содержание сообщения об ошибке"):
            assert update_quantity_body["message"] == "422 - error"

    @allure.story("Функциональность корзины")
    @allure.title("Добавление товара в корзину без авторизации")
    def test_add_product_without_auth(self):
        """
        Проверка обработки запроса на добавление товара в корзину без авторизации.

        Тест валидирует ошибку и структуру ошибки.
        """
        add_product = self.cart_api.add_product_without_auth(2425429)
        add_product_body = add_product.json()
        required_fields = {"message", "requestId"}
        has_all_fields = self.cart_api.check_fields_in_body(
            add_product_body, required_fields)

        with allure.step("Проверка структуры ошибки"):
            assert has_all_fields, "Некоторых полей не хватает в JSON."

        with allure.step("Содержание сообщения об ошибке"):
            assert add_product_body["message"] == "Authorization обязательное поле"

        with allure.step("Проверка статус-кода 401 Unauthorized"):
            assert add_product.status_code == 401

    @allure.story("Управление товарами в корзине")
    @allure.title("Удаление товара из корзины без авторизации")
    def test_delete_product_without_auth(self):
        """
        Проверка обработки запроса на удаление товара из корзины при отсутствии авторизации.

        Тест валидирует ошибку и структуру ошибки.
        """
        delete_product = self.cart_api.delete_product_without_auth(209211661)
        delete_product_body = delete_product.json()
        required_fields = {"message", "requestId"}
        has_all_fields = self.cart_api.check_fields_in_body(
            delete_product_body, required_fields)

        with allure.step("Проверка структуры ошибки"):
            assert has_all_fields, "Некоторых полей не хватает в JSON."

        with allure.step("Содержание сообщения об ошибке"):
            assert delete_product_body["message"] == "Authorization обязательное поле"

        with allure.step("Проверка статус-кода 401 Unauthorized"):
            assert delete_product.status_code == 401
