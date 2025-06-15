import pytest
import allure
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# from testdata.DataProvider import DataProvider
from configuration.ConfigProvider import ConfigProvider

# Извлечение конфигурационных данных
config_browser = ConfigProvider().get("ui", "browser_name")
config_timeout = ConfigProvider().get_int("ui", "timeout")

@pytest.fixture(scope="session")
def browser():
    """Фикстура для инициализации и закрытия браузера."""
    with allure.step("Открытие и настройка браузера"):
        if config_browser == "Chrome":
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        else:
            driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))
        driver.implicitly_wait(config_timeout)
        driver.maximize_window()
        yield driver
    with allure.step("Закрытие браузера"):
        driver.quit()

# @pytest.fixture(scope="session")

    # browser.find_element(By.XPATH,"//*[text()='Войти']").click()
# def login_as(self, email: str, password: str) -> None:
    # self.__driver.find_element(By.CSS_SELECTOR, "#username").send_keys(email)
    # self.__driver.find_element(By.CLASS_NAME, "css-178ag6o").click()
    # WebDriverWait(self.__driver, 10).until(
    #     EC.visibility_of_element_located((By.CSS_SELECTOR, "#password"))).send_keys(password)
    # self.__driver.find_element(By.CLASS_NAME, "css-178ag6o").click()

    # loginButton