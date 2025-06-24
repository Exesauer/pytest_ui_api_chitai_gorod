import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from testdata.DataProvider import DataProvider
from selenium.common.exceptions import TimeoutException


class Authorization:

    def __init__(self, driver: WebDriver) -> None:
        """
        Инициализирует страницу с предоставленным веб-драйвером.

        :param driver: WebDriver: Экземпляр веб-драйвера для управления браузером.
        """
        self.__driver = driver

    @allure.step("Авторизация пользователя с использованием номера телефона")
    def login_with(self) -> bool:
        """
        Выполняет процесс авторизации пользователя с помощью номера телефона.

        :returns: bool: True если имя пользователя корректно отобразилось на странице, иначе False.

        Процесс:
            1. Клик по элементу "Войти" на главной странице.
            2. Ввод номера телефона из параметров.
            3. Запрос кода подтверждения.
            4. Ожидание ввода кода подтверждения.
            5. Проверка успешной авторизации по имени пользователя из параметров.
        """
        with allure.step("Клик по элементу 'Войти'"):
            self.__driver.find_element(By.XPATH, "//*[text()='Войти']").click()

        with allure.step("Ввод номера телефона"):
            element = WebDriverWait(self.__driver, 10).until(
                EC.visibility_of_element_located(
                    (By.CSS_SELECTOR, "#tid-input"))
            )
            element.clear()
            element.send_keys(DataProvider().get("phone"))

        with allure.step("Запрос кода подтверждения"):
            WebDriverWait(self.__driver, 10).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//button[.//div[text()=' Получить код ']]"))
            )
            self.__driver.find_element(
                By.XPATH, "//button[.//div[text()=' Получить код ']]").click()
        try:
            with allure.step("Ожидание завершения авторизации и отображения имени пользователя"):
                check_user_name = WebDriverWait(
                    self.__driver,
                    60).until(
                    EC.text_to_be_present_in_element(
                        (By.XPATH,
                         "//span[@class='header-controls__text']"),
                        DataProvider().get("username")))
                return check_user_name

        except TimeoutException:
            return False
