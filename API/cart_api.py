import requests
import allure
from typing import Dict, List, Optional
from configuration.ConfigProvider import ConfigProvider
from testdata.DataProvider import DataProvider


class CartApi:
    """
    Класс предоставляет методы для взаимодействия с API корзины
    (просмотр, добавление, удаление товаров, обновление количества и др.).
    """

    def __init__(self):
        """Инициализация: Устанавливается URL корзины и заголовки для авторизации."""
        self.cart_url = ConfigProvider().get("api", "cart_url")
        self.headers = {
            "Authorization": DataProvider().get("token"),
            "User-Agent": ""
        }

    @allure.step("Просмотр содержимого корзины")
    def view_cart_contents(self) -> requests.Response:
        """
        Получает текущее содержимое корзины.

        :return: Response – объект ответа с текущим состоянием корзины.
        """
        response = requests.get(self.cart_url, headers=self.headers)

        allure.attach(
            response.text,
            name="Cart Contents",
            attachment_type=allure.attachment_type.JSON)

        return response

    @allure.step("Добавление продукта в корзину")
    def add_product_to_cart(self, product_id: int) -> requests.Response:
        """
        Добавляет продукт в корзину по его id.

        :param product_id: int – id добавляемого продукта.
        :return: Response – объект ответа.
        """
        payload = {
            "id": product_id
        }
        response = requests.post(
            self.cart_url + "/product", json=payload, headers=self.headers)

        allure.attach(
            response.request.body,
            name="Request Payload",
            attachment_type=allure.attachment_type.JSON)
        allure.attach(
            response.text,
            name="Response",
            attachment_type=allure.attachment_type.JSON)

        return response

    @allure.step("Удаление продукта из корзины")
    def delete_product_from_cart(
            self, cart_product_id: int) -> requests.Response:
        """
        Удаляет продукт из корзины по id корзинного объекта.

        :param cart_product_id: int – id товара в корзине.
        :return: Response – объект ответа.
        """
        response = requests.delete(
            self.cart_url +
            "/product/" +
            f"{cart_product_id}",
            headers=self.headers)

        allure.attach(
            response.text,
            name="Response",
            attachment_type=allure.attachment_type.JSON)

        return response

    @allure.step("Очистка корзины")
    def clear_cart(self) -> requests.Response:
        """
        Очищает всю корзину пользователя.

        :return: Response – объект ответа.
        """
        response = requests.delete(self.cart_url, headers=self.headers)

        allure.attach(
            response.text,
            name="Response",
            attachment_type=allure.attachment_type.JSON)

        return response

    @allure.step("Получение товара из корзины")
    def get_product_in_cart(self, product_id: int) -> Optional[Dict]:
        """
        Получает объект товара в корзине по его id (goodsId).

        :param product_id: int – id товара.
        :return: dict/None – данные о товаре в корзине либо None, если не найден.
        """
        products_in_cart = self.view_cart_contents().json().get('products', [])
        for product in products_in_cart:
            if product.get('goodsId') == product_id:
                return product
        return None

    def check_fields_in_body(self, body_data: Dict, fields: List[str]) -> bool:
        """
        Проверяет присутствие всех необходимых ключей в теле ответа.

        :param body_data: Dict – тело ответа.
        :param fields: List[str] – список ключей для проверки.
        :return: bool – True если все ключи присутствуют, иначе False.
        """
        return all(field in body_data for field in fields)

    @allure.step("Обновление количества товара")
    def update_quantity(
            self,
            cart_product_id,
            quantity: int) -> requests.Response:
        """
        Изменяет количество определённого товара в корзине.

        :param cart_product_id: int – id товара в корзине.
        :param quantity: int – новое количество.
        :return: Response – объект ответа.
        """
        payload = [
            {
                "id": cart_product_id,
                "quantity": quantity
            }
        ]
        response = requests.put(
            self.cart_url, json=payload, headers=self.headers)

        allure.attach(
            str(payload),
            name="Request Payload",
            attachment_type=allure.attachment_type.JSON)
        allure.attach(
            response.text,
            name="Response",
            attachment_type=allure.attachment_type.JSON)

        return response

    @allure.step("Получение всех товаров в корзине")
    def get_all_products_in_cart(self) -> List[Dict]:
        """
        Возвращает список всех товаров в корзине.

        :return: List[Dict] – список словарей с данными о товарах.
        """
        return self.view_cart_contents().json()["products"]

    @allure.step("Добавление товара без авторизации")
    def add_product_without_auth(self, product_id: int) -> requests.Response:
        """
        Пытается добавить товар в корзину без авторизации.

        :param product_id: int – id товара.
        :return: Response – объект ответа.
        """
        headers = {
            "Authorization": "",
            "User-Agent": ""
        }
        payload = {
            "id": product_id
        }
        response = requests.post(
            self.cart_url + "/product", json=payload, headers=headers)

        allure.attach(
            str(payload),
            name="Request Payload",
            attachment_type=allure.attachment_type.JSON)
        allure.attach(
            response.text,
            name="Response",
            attachment_type=allure.attachment_type.JSON)

        return response

    @allure.step("Удаление товара из корзины без авторизации")
    def delete_product_without_auth(
            self, cart_product_id: int) -> requests.Response:
        """
        Пытается удалить товар из корзины без авторизации.

        :param cart_product_id: int – id товара в корзине.
        :return: Response – объект ответа
        """
        headers = {
            "Authorization": "",
            "User-Agent": ""
        }
        response = requests.delete(
            self.cart_url +
            "/product/" +
            f"{cart_product_id}",
            headers=headers)

        allure.attach(
            response.text,
            name="Response",
            attachment_type=allure.attachment_type.JSON)

        return response

    @allure.step("Получение случайного id товара из топ-200")
    def get_random_id(self) -> int:
        """
        Метод получает случайный id товара из топ-200.

        :return: int – id товара.
        """
        url = "https://web-gate.chitai-gorod.ru/api/v2/products-top"
        my_params = {
            "topCount": 200,
            "resultCount": 1,
            "include": "productTexts,publisher,publisherBrand,publisherSeries,dates,literatureWorkCycle,rating"
        }
        response = requests.get(url, params=my_params, headers=self.headers)

        allure.attach(
            response.text,
            name="Response",
            attachment_type=allure.attachment_type.JSON)

        return response.json()["data"][0]["attributes"]["id"]
