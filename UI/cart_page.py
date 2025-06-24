import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class CartPage:

    def __init__(self, driver: WebDriver) -> None:
        """
        Инициализирует страницу с предоставленным веб-драйвером.

        :param driver: WebDriver: Экземпляр веб-драйвера для управления браузером.
        """
        self.__driver = driver

    @allure.step("Добавление товаров в корзину")
    def add_products_to_cart(self, count: int) -> None:
        """
        Добавляет указанное количество товаров в корзину.

        Метод находит кнопки "Купить" и кликает по ним, ожидая увеличения значения индикатора корзины после каждого клика.

        :param count: int: Количество товаров для добавления.
        """
        buttons_clicked = 0
        buy_buttons = WebDriverWait(
            self.__driver, 10).until(
            EC.presence_of_all_elements_located(
                (By.XPATH, "//div[@class='chg-app-button__content' and text()=' Купить']")))
        indicator_value = self.get_indicator_value()

        while buttons_clicked < count:

            for button in buy_buttons:
                with allure.step("Добавление товара в корзину'"):
                    self.__driver.execute_script(
                        "arguments[0].click();", button)

                    WebDriverWait(
                        self.__driver, 10).until(
                        lambda driver: self.get_indicator_value() == indicator_value + 1)

                indicator_value += 1
                buttons_clicked += 1

                if buttons_clicked >= count:
                    break

    @allure.step("Получение значения индикатора корзины")
    def get_indicator_value(self) -> int:
        """
        Функция получает значение индикатора корзины.

        :return: int: Значение индикатора корзины или 0, если элемент не найден.
        """
        indicator_element = self.__driver.find_elements(
            By.XPATH,
            "//div[contains(@class, 'chg-indicator') and contains(@class, 'chg-indicator--bg-cherry') and contains(@class, 'chg-indicator--mod-m-l') and contains(@class, 'header-controls__indicator')]")
        if indicator_element:
            return int(indicator_element[0].text)
        else:
            return 0

    @allure.step("Очистка корзины")
    def clear_cart(self) -> None:
        """
        Производит очистку корзины.

        Метод выполняет следующие действия
            -Ожидание видимости секции "Товары в наличии".
            -Клик на кнопку "Очистить корзину".
            -Ожидание появления сообщения о том, что корзина очищена.
        """
        with allure.step("Ожидание видимости секции 'Товары в наличии'"):
            WebDriverWait(
                self.__driver,
                10).until(
                EC.visibility_of_element_located(
                    (By.XPATH,
                     "//div[@class='cart-page__availability-title' and text()='Товары в наличии']")))

        with allure.step("Клик на кнопку 'Очистить корзину'"):
            self.__driver.find_element(
                By.XPATH,
                "//span[@class='cart-page__clear-cart-title' and text()='Очистить корзину']").click()

        with allure.step("Ожидание появления сообщения о том, что корзина очищена"):
            WebDriverWait(
                self.__driver,
                10).until(
                EC.visibility_of_element_located(
                    (By.XPATH,
                     "//p[@class='cart-multiple-delete__title' and text()='Корзина очищена']")))

    @allure.step("Получение итоговой суммы в корзине")
    def total_amount_cart(self) -> str:
        """
        Метод предназначен для получения итоговой суммы в корзине.

        Примечание:
            Если использовать этот метод до авторизации, а затем авторизоваться и сравнивать итоговую сумму с той, что
            отображается при оформлении заказа, будет несоответствие. Это связано с тем, что после авторизации
            изменяется размер скидки и, соответственно, итоговая сумма.

        :return: str: Итоговая сумма в виде строки.
        """
        with allure.step("Ожидание видимости итоговой суммы"):
            element = WebDriverWait(
                self.__driver,
                10).until(
                EC.visibility_of_element_located(
                    (By.XPATH,
                     "//div[@class='info-item cart-sidebar__item-summary']//div[@class='info-item__value']")))

            total = element.text
            return total

    @allure.step("Переход к процессу оформления заказа")
    def go_checkout(self) -> None:
        """
        Метод для перехода к процессу оформления заказа.

        Примечание: Требуется авторизация.

        Ожидает, пока кнопка "Перейти к оформлению" станет видимой, и выполняет клик по ней.
        """
        with allure.step("Ожидание видимости кнопки 'Перейти к оформлению' и выполнение клика"):
            WebDriverWait(
                self.__driver,
                10).until(
                EC.visibility_of_element_located(
                    (By.XPATH,
                     "//button[.//div[@class='chg-app-button__content' and text()=' Перейти к оформлению ']]"))).click()

    @allure.step("Попытка перехода к процессу оформления заказа без авторизации")
    def go_checkout_unauth(self) -> bool:
        """
        Метод производит попытку перенаправить пользователя к процессу офрмления заказа.

        Ожидает, пока кнопка "Перейти к оформлению" станет видимой, и выполняет клик по ней.

        :returns: bool: True если модальное окно аутентификации отобразилось, иначе False.
        """
        try:
            with allure.step("Ожидание видимости кнопки 'Перейти к оформлению' и выполнение клика"):
                WebDriverWait(
                    self.__driver,
                    10).until(
                    EC.visibility_of_element_located(
                        (By.XPATH,
                         "//button[.//div[@class='chg-app-button__content' and text()=' Перейти к оформлению ']]"))).click()

            with allure.step("Ожидание отображения модального окна аутентификации"):
                modal_element = WebDriverWait(self.__driver, 10).until(
                    EC.visibility_of_element_located(
                        (By.XPATH, "//p[@class='auth-modal-content__text']"))
                )
            return True if modal_element.is_displayed() else False

        except TimeoutException:
            return False

    @allure.step("Получение итоговой суммы при оформлении заказа")
    def total_amount_order(self) -> str:
        """
        Метод для получения итоговой суммы при оформлении заказа.

        :return: str: Итоговая сумма в виде строки.
        """
        with allure.step("Ожидание видимости итоговой суммы"):
            element = WebDriverWait(
                self.__driver,
                10).until(
                EC.visibility_of_element_located(
                    (By.XPATH,
                     "(//div[@data-v-e74c0fec and contains(@class, 'checkout-summary__col')])[2]")))

            total = element.text
            return total

    @allure.step("Получение количества товаров в корзине")
    def get_cart_items_count(self) -> int:
        """
        Метод для получения количества элементов, соответствующих товарам в корзине.

        :returns: int: Количество товаров в корзине или 0, если элементы не найдены.
        """
        with allure.step("Поиск элементов, соответствующих товарам в корзине"):
            cart_items_count = len(
                self.__driver.find_elements(
                    By.XPATH, "//div[@class='cart-item']"))
            return cart_items_count
