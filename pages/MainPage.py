import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from configuration.ConfigProvider import ConfigProvider

config_base_url = ConfigProvider().get("ui", "base_url")

class MainPage:

    def __init__(self, driver: WebDriver) -> None:
        self.__url = config_base_url
        self.__driver = driver

    @allure.step("Переход на главную страницу магазина")
    def go_main_page(self) -> None:
        self.__driver.get(self.__url)
