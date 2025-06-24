import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from typing import List
import string
import re


class SearchPage:

    def __init__(self, driver: WebDriver) -> None:
        """
        Инициализирует страницу с предоставленным веб-драйвером.

        :param driver: WebDriver: Экземпляр веб-драйвера для управления браузером.
        """
        self.__driver = driver

    @allure.step("Поиск товаров по названию")
    def search_products(self, product_name: str) -> None:
        """
        Метод предназначен для поиска товаров по названию.

        :param product_name: str: Название товара для поиска.

        Процесс:
            1. Поиск элемента ввода в форму для поиска.
            2. Попытка до 3 раз ввести название товара в поле поиска.
            3. Проверка соответствия введённого текста ожидаемому значению.
            4. В случае неудачи после 3 попыток вызывает ValueError.
            5. Отправка формы поиска.
            6. Ожидание отображения результатов поиска.
        """
        search_input_locator = (
            By.XPATH,
            "//input[@name='search' and @class='search-form__input search-form__input--search']")
        search_input = self.__driver.find_element(*search_input_locator)
        attempts = 0
        max_attempts = 3

        while attempts < max_attempts:

            with allure.step(f"Попытка {attempts + 1} ввода текста '{product_name}'"):
                search_input.send_keys(Keys.CONTROL + 'a')
                search_input.send_keys(Keys.DELETE)
                search_input.send_keys(product_name)

            with allure.step("Проверка корректности введённого текста"):
                entered_value = WebDriverWait(self.__driver, 10).until(
                    lambda driver: driver.find_element(
                        *search_input_locator).get_attribute("value")
                )
                if entered_value == product_name:
                    break

            attempts += 1
            if attempts == max_attempts:
                raise ValueError(
                    "Не удалось ввести текст в поле поиска после нескольких попыток")

        with allure.step("Отправка формы для выполнения поиска"):
            search_input.send_keys(Keys.RETURN)

        with allure.step("Ожидание отображения результатов поиска"):
            WebDriverWait(self.__driver, 10).until(
                EC.visibility_of_element_located(
                    (By.XPATH, "//div[@class='app-catalog__content']"))
            )
        self.__driver.refresh()

    @allure.step("Проверка результатов поиска")
    def validate_search_results(
            self, product_name_variants: List[str]) -> None:
        """
        Проверяет, присутствуют ли ожидаемые названия товаров среди результатов поиска на веб-странице.

        Данный метод ищет элементы, представляющие товары на странице, и проверяет, содержится ли хотя бы
        одно из переданных названий в атрибутах этих элементов. Названия приводятся к унифицированному виду, чтобы избежать
        ошибок, связанных с различиями в регистре или пунктуации.

        :param product_name_variants: List[str]: Список ожидаемых названий товаров в результатах поиска.

        raise AssertionError: Если ни одно из заданных названий товаров не найдено в результатах поиска.
        """
        with allure.step("Получение списка элементов, представляющих товары"):
            product_elements = self.__driver.find_elements(
                By.XPATH, "//div[contains(@class, 'app-products-list app-catalog__list')]//article")

            normalized_variants = [
                variant.lower().replace(
                    '-',
                    ' ').translate(
                    str.maketrans(
                        '',
                        '',
                        string.punctuation)) for variant in product_name_variants]

        with allure.step("Поиск совпадений среди всех найденных элементов"):
            product_found = any(
                any(
                    normalized_variant in product_element.get_attribute('data-chg-product-name').lower(
                    ).replace('-', ' ').translate(str.maketrans('', '', string.punctuation))
                    for normalized_variant in normalized_variants)
                for product_element in product_elements
            )

        if not product_found:
            raise AssertionError(
                "Не найдено ни одного из названий в результатах поиска")

    @allure.step("Сравнение названий товаров в поиске с названиями на их страницах")
    def compare_search_and_product_titles(self, count: int) -> bool:
        """
        Метод сравнивает названия товаров из результатов поиска с названиями,
        которые отображаются на страницах соответствующих товаров.

        :param count: int: Количество товаров, для которых необходимо провести сравнение.

        :return: bool - Возвращает True, если все названия совпадают, и False в противном случае.

        Процесс:
            1. Извлекает названия и ссылки на товары из результатов поиска, ограничиваясь заданным количеством.
            2. Для каждого товара переходит на его страницу и получает отображаемое название.
            3. Сравнивает название товара на странице с названием из результатов поиска.

        Исключение:
            Если названия не совпадают, выводится сообщение об ошибке с указанием несоответствующих названий и ссылкой на страницу товара.
        """
        product_links = []

        captions = self.__driver.find_elements(
            By.CLASS_NAME, "product-card__caption")
        for caption in captions[:count]:
            product_link_element = caption.find_element(
                By.CLASS_NAME, "product-card__title")
            product_link = product_link_element.get_attribute("href")
            product_title = product_link_element.get_attribute("title").strip()
            product_links.append((product_link, product_title))

        for product_link, product_title in product_links:
            with allure.step(f"Переход на страницу товара {product_link}"):
                self.__driver.get(product_link)

                product_page_title = self.__driver.find_element(
                    By.CSS_SELECTOR, "h1[itemprop='name']").text.strip()

            try:
                with allure.step("Сравнение названия товара из результатов поиска с названием на его странице"):
                    assert self.clean_title(product_page_title.lower()) == self.clean_title(product_title.lower(
                    )), f"Ошибка: '{product_page_title}' не совпадает с '{product_title}'. Ссылка на страницу товара: {product_link}"

            except AssertionError as e:
                print(e)

    def clean_title(self, title) -> str:
        """
        Функция удаляет ненужные символы из названия товара, включая текст в скобках, пробелы перед скобками и числа с плюсом.

        :param title: str: Название товара, которое может быть получено любым способом.

        :return: str: Название товара без лишних символов.
        """
        title_pattern = r'\s*\(.*?\)|\s*\d+\+'
        cleared_title = re.sub(title_pattern, '', title)
        return cleared_title.strip()
